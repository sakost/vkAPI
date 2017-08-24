**The interface is like the interface of library** *"vk"*::

    >>>import vkAPI

    >>>session = vkAPI.Session('<access_token>'[, '<secret>'])

    >>>api = vkAPI(session[, v='5.68'][, ...])

    >>>api.messages.send(user_id=<user_id>, message='<message>')
    2134837

**It has a newer method to auth with login and password(it works much faster than at the** *"vk"*::

    >>>import vkAPI

    >>>session = AuthSession('<user_login>', 'user_password'[, app_id=<app_id>][, scope='all'][, lang='ru'][, client_secret='<secret>'])
    ...

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

