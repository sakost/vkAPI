import time

import unittest

import vkAPI as vk
import vkAPI.utils as utils

USER_LOGIN = ''         # user email or phone number
USER_PASSWORD = ''      # user password
APP_ID = ''             # aka API/Client ID


class UtilsTestCase(unittest.TestCase):
    def test_stringify(self):
        self.assertEqual({1: 'str,str2'}, utils.stringify_values({1: ['str', 'str2']}))

    def test_stringify_2(self):
        self.assertEqual({1: 'str,стр2'}, utils.stringify_values({1: ['str', 'стр2']}))

    def test_stringify_3(self):
        self.assertEqual({1: 'стр,стр2'}, utils.stringify_values({1: ['стр', 'стр2']}))


class VkTestCase(unittest.TestCase):

    def setUp(self):
        auth_session = vk.AuthSession(app_id=APP_ID, user_login=USER_LOGIN, user_password=USER_PASSWORD)
        access_token, _ = auth_session.access_token

        session = vk.Session(access_token=access_token)
        self.vk_api = vk.API(session, lang='ru')

    def test_get_server_time(self):
        time_1 = time.time() - 1
        time_2 = time_1 + 10
        server_time = self.vk_api.getServerTime()
        self.assertTrue(time_1 <= server_time <= time_2)

    def test_get_server_time_via_token_api(self):
        time_1 = time.time() - 1
        time_2 = time_1 + 10
        server_time = self.vk_api.getServerTime()
        self.assertTrue(time_1 <= server_time <= time_2)

    def test_get_profiles_via_token(self):
        profiles = self.vk_api.users.get(user_id=1)
        self.assertEqual(profiles[0]['last_name'], 'Дуров')


if __name__ == '__main__':
    unittest.main()


