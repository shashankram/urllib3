import unittest

from threading import Lock

from dummyserver.server import (
    make_server_thread,
    make_wsgi_server, socket_server,
    DEFAULT_CERTS,
)


# TODO: Change ports to auto-allocated?


class SocketDummyServerTestCase(unittest.TestCase):
    """
    A simple socket-based server is created for this class that is good for
    exactly one request.
    """
    scheme = 'http'
    host = 'localhost'
    port = 18080

    @classmethod
    def _start_server(cls, socket_handler):
        ready_lock = Lock()
        cls.server_thread = make_server_thread(socket_server,
                                               socket_handler=socket_handler,
                                               host=cls.host, port=cls.port)

        ready_lock.acquire()

class HTTPDummyServerTestCase(unittest.TestCase):
    scheme = 'http'
    host = 'localhost'
    host_alt = '127.0.0.1' # Some tests need two hosts
    port = 18081
    certs = DEFAULT_CERTS

    @classmethod
    def _start_server(cls):
        cls.server_thread = make_server_thread(make_wsgi_server,
                                               host=cls.host, port=cls.port,
                                               scheme=cls.scheme,
                                               certs=cls.certs)

        # TODO: Loop-check here instead
        import time
        time.sleep(0.1)

    @classmethod
    def _stop_server(cls):
        import urllib # Yup, that's right.
        try:
            urllib.urlopen(cls.scheme + '://' + cls.host + ':' + str(cls.port) + '/shutdown')
        except IOError:
            pass
        cls.server_thread.join()


    @classmethod
    def setUpClass(cls):
        cls._start_server()

    @classmethod
    def tearDownClass(cls):
        cls._stop_server()


class HTTPSDummyServerTestCase(HTTPDummyServerTestCase):
    scheme = 'https'
    host = 'localhost'
    port = 18082
    certs = DEFAULT_CERTS