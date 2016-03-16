import json
from bson import ObjectId
from tornado.testing import gen_test
from test.testbase import TestBaseHandler


class TestReport(TestBaseHandler):
    @gen_test
    def test_report_good_request(self):
        _id = "36636c72346a393832343334"
        data = {"_id": _id}
        body = json.dumps(data)
        response = yield self.http_client.fetch(self.get_url("/api/report"), method="POST", body=body)
        self.assertEqual(response.code, 200)
        response = json.loads(response.body.decode())
        self.assertEqual(response['status'], 200)

    @gen_test
    def test_report_bad_request(self):
        _id = ObjectId()
        data = {"_id": _id.__str__()}
        body = json.dumps(data)
        response = yield self.http_client.fetch(self.get_url("/api/report"), method="POST", body=body)
        self.assertEqual(response.code, 200)
        response = json.loads(response.body.decode())
        self.assertEqual(response['status'], 500)



