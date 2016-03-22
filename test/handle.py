import json
from tornado.testing import gen_test
from test.base import TestBaseHandler


class TestHandler(TestBaseHandler):
    @gen_test
    def test_handler(self):
        expected_response=dict(
            code=200,
            body=dict(
                status=200
            )
        )
        self.check("/",method="GET",headers=None,expected_response=expected_response)
