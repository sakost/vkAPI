from vkAPI.exceptions import *
from vkAPI.utils import *


class AuthMixin(object):
    OAUTH_URL = 'https://oauth.vk.com/token'

    def __init__(self, user_login='', user_password='', app_id=2274003, scope='offline', client_secret='hHbZxrka2uZ6jB1inYsH',
                 lang='ru'):
        """
        :param app_id: Id of vk app. Default app id of Android official app
        :param user_login: User Login
        :param user_password: User password
        :param scope: Scopes that needs to get access to some methods
        :param client_secret: Client app secret. Optional. 
        If you use your own app and app id, please keep this parameter as None
        
        :type app_id: int
        :type user_login: str
        :type user_password: str
        :type scope: str
        :type client_secret: str
        :type lang: str
        """
        self._app_id = app_id
        self._ulog = user_login
        self._upas = user_password
        self._scope = scope
        self._client_secret = client_secret
        self._lang = lang
        self._make_auth_request()

    def _make_auth_request(self):
        params = {
            'username': self._ulog,
            'password': self._upas,
            'scope': self._scope,
            '2fa_supported': 1,
            'device_id': '',
            'libverify_support': 1,
            'grant_type': 'password',
            'client_secret': self._client_secret,
            'client_id': self._app_id,
            'lang': self._lang
        }
        response = VkRequest().get(self.OAUTH_URL, params=params)
        response = response.json()
        if response.get('error'):
            raise VkAuthError(response)
        self._expires_in = response.get('expires_in')
        self.access_token = response['access_token']
        self._secret = response.get('secret')

