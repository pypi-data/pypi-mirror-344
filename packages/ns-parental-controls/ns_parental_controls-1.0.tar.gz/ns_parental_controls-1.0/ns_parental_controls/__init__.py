import time
from urllib.parse import urlencode

import requests

from ns_parental_controls.const import CLIENT_ID, REDIRECT_URI, SCOPE, AUTHORIZE_URL, SESSION_TOKEN_URL, TOKEN_URL, \
    GRANT_TYPE, MY_ACCOUNT_ENDPOINT, USER_AGENT, MOBILE_APP_PKG, OS_NAME, OS_VERSION, DEVICE_MODEL, MOBILE_APP_VERSION, \
    MOBILE_APP_BUILD, ENDPOINTS, BASE_URL
from ns_parental_controls.helpers import random_string, hash_it, parse_response_url


class ParentalControl:
    '''
    This will allow you to enable/disable a device.
    Its based on the mobile app api so you have to do some wonky
    copy/paste to make it work, but its not too bad for techies.
    '''

    def __init__(self, save_state_callback=None, load_state_callback=None, callback_kwargs={}):
        '''
        If you need to re-hydrate this object, you can use
        the save/load callbacks to restore the state.

        :param save_state_callback (Callable[[dict], None]):
        :param load_state_callback (Callable[[dict], dict]):
        :param callback_kwargs (dict): Some additional metadata that will be included in the save/load callbacks. Can be useful for storing a userId or something.
        '''
        self.save_state_callback = save_state_callback
        self.load_state_callback = load_state_callback
        self.callback_kwargs = callback_kwargs

        self.verification_code = None
        self.session_token = None
        self.access_token = None
        self.access_token_expires_timestamp = 0
        self.id_token = None
        self.account_id = None

        self._load()

    def get_auth_url(self):
        '''
        The user should go to this link.
        Assuming you are already logged in, you will
        see a "select this account" button.
        Right-click on that button and copy the link.
        You will paste that link into process_auth_link() method.
        :return str: The login url that you can click on.
        '''
        # Generate a temporary code that will be used to verify
        # the server response.
        # That way we know the response actually came from the server.
        self.verification_code = random_string()
        self._save(verification_code=self.verification_code)

        # build the login url
        params = {
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "session_token_code",
            "scope": SCOPE,
            "session_token_code_challenge": hash_it(self.verification_code),
            "session_token_code_challenge_method": "S256",
            "state": self.verification_code,
            "theme": "login_form"
        }
        login_url = AUTHORIZE_URL.format(urlencode(params)).replace("%2B", "+")
        return login_url

    def process_auth_link(self, link: str):
        '''
        This will use the link to get the needed tokens.
        :param link (str): string like 'npf54789befb391a838://auth#session_token_code=really-long-string&state=verification-code-here&session_state=abc123-'
        :return None:
        '''
        # pull out the important info from the link
        data = parse_response_url(link)
        data['client_id'] = CLIENT_ID
        data['session_token_code_verifier'] = self.verification_code

        # trade our session_token_code for a session_token
        resp = requests.post(
            url=SESSION_TOKEN_URL,
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'User-Agent': 'NASDKAPI; Android',
            }
        )
        self.session_token = resp.json().get('session_token')
        self._save(session_token=self.session_token)

        self.get_new_access_token()

    def get_new_access_token(self):
        '''
        Used to get either a new access token or to refresh an expired access token.
        This is called by the needed methods, you should not need to call directly.
        :return str: The access token used for HTTP requests
        '''
        # trade the session_token for an access_token

        resp = requests.post(
            url=TOKEN_URL,
            json={
                "client_id": CLIENT_ID,
                "grant_type": GRANT_TYPE,
                "session_token": self.session_token
            }
        )
        if not resp.ok:
            print(resp.text)

        self.access_token = resp.json()['access_token']
        self.id_token = resp.json()['id_token']
        self.access_token_expires_timestamp = (
                time.time() + resp.json()['expires_in']
        )

        self._save(
            access_token=self.access_token,
            id_token=self.id_token,
            access_token_expires_timestamp=self.access_token_expires_timestamp
        )

        return self.access_token

    def _save(self, **kwargs):
        '''
        Makes a call to the save_state_callback.
        You can use this to sore the state somewhere (in your database/filesystem presumably)
        :param kwargs (dict): kwargs you want to save, these will be appended/overwritten to the existing state
        :return None:
        '''
        if self.save_state_callback:
            d = self._load().copy()
            d.update(**kwargs)
            self.save_state_callback(**d)

    def _load(self):
        '''
        Used to load the state from your database.
        :return dict: The state that is saved in the db, also initializes internal values like self.access_token
        '''
        if self.load_state_callback:
            data = self.load_state_callback(**self.callback_kwargs)

            self.verification_code = data.get('verification_code', None) or random_string()
            self.session_token = data.get('session_token', None)

            self.access_token = data.get('access_token', None)
            self.id_token = data.get('id_token', None)
            self.access_token_expires_timestamp = data.get('access_token_expires_timestamp', 0)

            self.account_id = data.get('account_id', None)
            return data
        else:
            self.verification_code = random_string()

        return {'verification_code': self.verification_code}

    def get_access_token(self):
        '''
        Use this to access the current token.
        This will handle any logic for refreshing a token that is expired.
        :return str:
        '''
        if self.access_token and self.access_token_expires_timestamp < time.time():
            # the access token exist and is not expired
            return self.access_token
        else:
            # the access token is missing or expired
            time.sleep(1)
            return self.get_new_access_token()

    def get_account_id(self):
        '''
        Get the user's account_id.
        This is needed for some other HTTP requests.
        You shouldnt have to call this directly.
        :return str:
        '''
        if self.account_id is None:
            resp = requests.get(
                url=MY_ACCOUNT_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {self.get_access_token()}"
                }
            )
            print('resp=', resp)
            print(resp.json())
            self.account_id = resp.json()['id']
            self._save(account_id=self.account_id)

        return self.account_id

    def send_request(self, method='GET', *a, **k):
        '''
        All API requests go through here.
        It handles authentication and headers and such.

        Note that if the request fails because of an invalid_token,
        this will refresh the token and try again 3 times.

        :param method (str): 'get' 'post', etc
        :param a:
        :param k:
        :return requests.Response: The response object from the server.
        '''
        i = 3
        while i > 0:
            i -= 1
            resp = requests.request(
                method=method,
                headers={
                    "Authorization": 'Bearer ' + self.get_access_token(),
                    "User-Agent": USER_AGENT,
                    "X-Moon-App-Id": MOBILE_APP_PKG,
                    "X-Moon-Os": OS_NAME,
                    "X-Moon-Os-Version": OS_VERSION,
                    "X-Moon-Model": DEVICE_MODEL,
                    "X-Moon-TimeZone": str(time.timezone),
                    "X-Moon-Os-Language": 'en-US',
                    "X-Moon-App-Language": 'en-US',
                    "X-Moon-App-Display-Version": MOBILE_APP_VERSION,
                    "X-Moon-App-Internal-Version": MOBILE_APP_BUILD,
                },
                *a, **k
            )
            if resp.ok:
                return resp
            elif 'invalid_token' in resp.text:
                self.get_new_access_token()
            time.sleep(1)

    def get_device(self, device_label: str):
        '''
        Get a list of device dicts.
        :param device_label (str): The name of the device
        :return dict | None: The device dict (should prob make this a proper object)
        '''
        # get the list of devices

        resp = self.send_request(
            'GET',
            url=ENDPOINTS['get_account_devices']['url'].format(
                BASE_URL=BASE_URL,
                ACCOUNT_ID=self.get_account_id()
            )

        )
        if not resp.ok:
            print('error getting device', resp.text)

        for dev in resp.json().get('items', []):
            if dev.get('label', '') == device_label:
                print('found device=', dev)
                return dev
        else:
            print('device not found')
            for dev in resp.json().get('items', []):
                print('dev=', dev)
        return None

    def get_parental_control_settings(self, device):
        data = self._load()
        if device['deviceId'] not in data:

            resp = self.send_request(
                'GET',
                url=BASE_URL + '/devices/' + device.get('deviceId') + '/parental_control_setting',

            )
            if resp.ok:
                print('get_parental_control_settings success')
                print(resp.json())

                self._save(**{
                    device['deviceId']: resp.json()
                })
                data.update({
                    device['deviceId']: resp.json()
                })
            else:
                print('get settings failed', resp.text)
        print('old settings=', data[device['deviceId']])
        return data[device['deviceId']]

    def lock_device(self, device_label: str, lock: bool):
        '''
        This is shown as "Disable Alarms for Today" in the app.
        :param device_label (str): The name of the device
        :param lock (bool): True means disable the device, False means enable the device.
        :return None:
        '''
        device = self.get_device(device_label)

        resp = self.send_request(
            "POST",
            url=BASE_URL + '/devices/' + device.get('deviceId') + '/alarm_setting_state',
            json={'status': 'TO_VISIBLE' if lock else 'TO_INVISIBLE'}
        )
        if resp.ok:
            pass
        else:
            print(resp.reason)
            print(resp.headers)
            print(resp.content)

        print('lock_device', lock, 'ok=', resp.ok)
