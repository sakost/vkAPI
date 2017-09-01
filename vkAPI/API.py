import hashlib

from vkAPI.mixins import *
from vkAPI.utils import *


class Session(object):
    """A Session object where you should put a default params which will always send"""
    API_URL = 'https://api.vk.com/method/'

    def __init__(self, access_token=None, secret=None):
        """
        :except kwargs: such params as 'lang' or 'https'
        
        :param access_token: access token
        :param secret: a 'secret' parameter
        
        :type access_token: str
        :type secret: str
        """
        self.access_token = access_token
        self._session_request = VkRequest()
        if secret:
                self._secret = secret

    def __str__(self):
        return '<Session of vkAPI>'

    @staticmethod
    def get_md5_hash(string):
        return hashlib.md5(string.encode()).hexdigest()

    @staticmethod
    def get_sig_data(method, secret, params=None):
        if params is None:
            params = {}
        data = ''
        for key, item in params.items():
            data += str(key) + '=' + str(item) + '&'
        data = data[:-1]
        data += '&sig=' + Session.get_md5_hash('/method/' + method + '?' + data + secret)
        return data

    def _make_request(self, method_request):
        req = self._send_request(method_request)
        req.raise_for_status()
        text = Parser(req.text).start()
        for error_or_response in json_iter_parse(text):
            if 'response' in error_or_response:
                return error_or_response['response']
            elif 'error' in error_or_response:
                error = VkAPIError(error_or_response)

                if error.is_access_token_incorrect():
                    self.access_token = None
                    return self._make_request(method_request)

                raise error

    def _send_request(self, request):
        url = self.API_URL + request._method_name
        method_args = request._api._method_default_args.copy()
        method_args.update(request._method_args)
        access_token = self.access_token
        if access_token:
            method_args['access_token'] = access_token
        if hasattr(self, '_secret'):
            if self._secret is not None:
                method_args = self.get_sig_data(request._method_name, self._secret, method_args)
        timeout = request._api._timeout
        response = self._session_request.post(url, method_args, timeout=timeout)
        return response

    def __setattr__(self, key, value):
        if key == 'API_URL':
            raise AttributeError('"' + key + '" doesn\'t support assignment')
        self.__dict__[key] = value


class API(object):
    def __init__(self, session, timeout=10, v='5.68', **method_default_args):
        """
        :param session: Object Session
        :param timeout: timeout. 10 by default
        :param v: API version
        :param method_default_args: Default args that will be used always in this API object
        
        :type session: Session
        :type timeout: int
        :type v: str
        """
        self._session = session
        self._timeout = timeout
        self._method_default_args = method_default_args
        self._method_default_args.update({'v': v})

    def __getattr__(self, method_name):
        return Request(self, method_name)

    def __call__(self, method_name, **method_kwargs):
        return getattr(self, method_name)(**method_kwargs)


class Decorator(API):
    def __getattr__(self, method_name):
        return DecorRequest(self, method_name)

    def __call__(self, method_name, **method_kwargs):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, getattr(self, method_name)(**method_kwargs), **kwargs)
            return wrapper
        return decorator


class Request(object):
    __slots__ = ('_api', '_method_name', '_method_args')

    def __init__(self, api, method_name):
        self._api = api
        self._method_name = method_name

    def __getattr__(self, method_name):
        return Request(self._api, self._method_name + '.' + method_name)

    def __call__(self, **method_args):
        self._method_args = method_args
        return self._api._session._make_request(self)


class DecorRequest(Request):
    def __getattr__(self, method_name):
        return DecorRequest(self._api, self._method_name + '.' + method_name)

    def __call__(self, is_method=False, **method_args):
        self._method_args = method_args

        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, self._api._session._make_request(self), **kwargs)
            return wrapper
        return decorator


class AuthSession(AuthMixin, Session):
    def __init__(self, user_login='', user_password='', app_id=2274003, scope='offline', client_secret='hHbZxrka2uZ6jB1inYsH',
                 lang='ru'):
        AuthMixin.__init__(self, user_login, user_password, app_id, scope, client_secret, lang)
        access_token = self.access_token
        secret = self._secret
        Session.__init__(self, access_token, secret)
        self.access_token = access_token

    def __setattr__(self, key, value):
        if key == 'OAUTH_URL' or key == 'API_URL':
            raise AttributeError('"' + key + '" doesn\'t support assignment')
        self.__dict__[key] = value
