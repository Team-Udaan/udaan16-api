import json
from tornado.testing import gen_test
from test.testbase import TestBaseHandler


class TestHandler(TestBaseHandler):
    @gen_test
    def test_handler(self):
        response = yield self.http_client.fetch(self.get_url("/"))
        self.assertEqual(response.code, 200)
        body = response.body.decode()
        response = json.loads(body)
        self.assertEqual(response['status'], 200)