import json
import os

from tornado.gen import coroutine
from tornado.ioloop import IOLoop

import server
from tornado.testing import AsyncHTTPTestCase, gen_test


class TestBaseHandler(AsyncHTTPTestCase):

    os.environ["ASYNC_TEST_TIMEOUT"] = "60"

    def get_db_client(self):
        return server.client

    def get_app(self):
        return server.get_app()

    def get_http_server(self):
        return server.get_http_server(self.get_app())

    def get_new_ioloop(self):
        return IOLoop.current()

    def get_http_port(self):
        return server.port

    #
    # @gen_test
    # def test_home(self):
    #     yield self.check("/", "GET", None, {
    #         "code": 200,
    #         "body": dict(
    #             message="Not Implemented",
    #             status=501
    #         )})

    @coroutine
    def check(self, path, method, headers, expected_response, body=None):
        http_client = self.get_http_client()
        response = yield http_client.fetch(self.get_url(path), method=method, headers=headers,body=body)
        self.assertEqual(response.code, expected_response["code"])
        response_body = json.loads(response.body.decode())
        self.assertEqual(response_body, expected_response["body"])
