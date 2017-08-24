AUTHORIZATION_FAILED = 5    # Invalid access token


class VkError(Exception):
    pass


class VkAuthError(VkError):
    def __init__(self, data):
        super().__init__()
        self.string = data['error_description']

    def __str__(self):
        return self.string


class VkAPIError(VkError):
    CAPTCHA_NEEDED = 14
    ACCESS_DENIED = 15

    def __init__(self, data):
        super().__init__('')
        self.data = data['error']
        self.error_code = str(self.data['error_code'])
        self.error_msg = self.data['error_msg']
        self.request_params = self.get_req_params()

    def get_req_params(self):
        dictionary = {}
        for param in self.data['request_params']:
            dictionary.update({param['key']: param['value']})
        return dictionary

    def is_access_token_incorrect(self):
        return self.error_code == self.ACCESS_DENIED and 'access_token' in self.error_msg

    def __str__(self):
        message = self.error_code + '. ' + self.error_msg + '\nRequested parameters:\n'
        for key, value in self.request_params.items():
            message += key + ' = ' + value + ',\n'
        message = message[:-2]
        return message
