from tornado.ioloop import IOLoop

import server
from tornado.testing import AsyncHTTPTestCase, gen_test


class TestBaseHandler(AsyncHTTPTestCase):

    def get_db_client(self):
        return server.client

    def get_app(self):
        return server.get_app()

    def get_http_server(self):
        return server.get_http_server(self._app)

    def get_new_ioloop(self):
        return IOLoop.current()

    def get_http_port(self):
        return server.options.port

    @gen_test
    def test(self):
        self.assertEqual(True, True)
