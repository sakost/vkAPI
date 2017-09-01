from vkAPI.messages import LongPoll
from vkAPI.API import Session, API, AuthSession, Decorator
__str__ = 'vkAPI module to easier work with API of VK'
__author__ = "Mr Morg@n"
__version__ = '1.3.0'
__all__ = []
__doc__ = """
**The interface is like the interface of library** *"vk"*::

    >>>import vkAPI

    >>>session = vkAPI.Session('<access_token>'[, '<secret>'])

    >>>api = vkAPI(session[, v='5.68'][, ...])

    >>>api.messages.send(user_id=<user_id>, message='<message>')
    2134837

**It has a newer method to auth with login and password(it works much faster than at the** *"vk"*)::

    >>>import vkAPI

    >>>session = AuthSession('<user_login>', 'user_password'[, app_id=<app_id>][, scope='all'][, lang='ru'][, client_secret='<secret>'])
    ...

**It has a class of decorator**::

    >>>import vkAPI

    >>> session = ...

    >>>decorator = vkAPI.Decorator(session)

    >>>@decorator.users.get(user_ids='...')
    ...def callback(callback_data):
    ...    print(callback_data)
    >>>callback()
    [...]
    >>>class Test:
    ...    @decorator.users.get(user_ids='...')
    ...    def callback(self, callback_data):
    ...        print(callback_data)
    
    >>>Test().callback()
    [...]
    
The callback data must be at the end of users function/method

**It also has a LongPoll support**::

    >>>import vkAPI

    >>>longpoll = LongPoll(<access_token>[, using='multiprocessing']) # You can also use threading

    >>>longpoll.create_session()

    >>>longpoll.run_session()

    >>>for num, update in longpoll.iter_updates():
    ...    if num == 10:
    ...        break
    ...    print(update)
    ...
    >>>longpoll.stop_session()

    >>>with LongPoll('access_token', 'multiprocessing') as longpoll:
          ...

"""
