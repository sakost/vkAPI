import time

from vkAPI.utils import VkRequest
from vkAPI.exceptions import *


class LongPoll:
    API_URL = 'https://api.vk.com/method/'

    def __init__(self, access_token, using='threading'):
        """
        :param access_token: to call methods from vk api
        :param using: to use multiprocessing or threading
        
        :type access_token: str
        :type using: str
        """
        self.access_token = access_token
        self.multi = using.lower()
        self._session = None
        self._event = None
        self._queue = None

    def create_session(self):
        process = None
        Queue = None
        if self.multi == 'multiprocessing':
            import multiprocessing
            process = multiprocessing.Process
            Queue = multiprocessing.Queue()
            e = multiprocessing.Event()
        elif self.multi == 'threading':
            import threading, queue
            process = threading.Thread
            Queue = queue.Queue()
            e = threading.Event()
        else:
            raise ValueError('A "multiprocessing" attribute must be equals to "multiprocessing" or "threading"')

        class Session(process):
            def __init__(self, access_token, q, event):
                super(Session, self).__init__()
                self.access_token = access_token
                self.dir = []
                self.queue = q
                self.event = event
                self.request = VkRequest()

            def run(self):
                req = self.request.post(LongPoll.API_URL + 'messages.getLongPollServer', params={
                    'lp_version': 2,
                    'access_token': self.access_token,
                    'v': '5.68'
                })
                req = req.json()
                try:
                    req = req['response']
                except KeyError:
                    raise VkAPIError(req)
                while not self.event.is_set():
                    LP_URL = 'https://%(server)s?act=a_check&key=%(key)s&ts=%(ts)s&wait=25&mode=2&version=2' % req
                    response = self.request.get(LP_URL, timeout=25).json()
                    req['ts'] = response['ts']
                    for element in response['updates']:
                        self.queue.put(element)
        self._event = e
        self._queue = Queue
        self._session = Session(self.access_token, Queue, e)

    def run_session(self):
        self._session.start()

    def stop_session(self):
        self._event.set()

    def iter_updates(self):
        i = -1
        while True:
            if self._queue.qsize == 0:
                time.sleep(1)
                continue
            var = self._queue.get()
            i += 1
            yield var, i

    def __enter__(self):
        self.run_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_session()
        if exc_val:
            raise exc_val
