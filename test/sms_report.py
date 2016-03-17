import json
from datetime import datetime
from urllib.parse import urlencode
from bson import ObjectId
from tornado.testing import gen_test
from test.base import TestBaseHandler


class TestReport(TestBaseHandler):

    @gen_test
    def test_report_valid_request(self):
        client = self.get_db_client()
        number = "9123456789"
        _id = client.sms.smsCollection.insert({"number": number})
        data = {
            "number": number,
            "customID": _id,
            "status": "D",
            "datetime": datetime.now().timestamp()
        }
        body = urlencode(data)
        response = yield self.http_client.fetch(self.get_url("/api/report"), method="POST", body=body)
        response = json.loads(response.body.decode())
        self.assertEqual(response['status'], 200)
        client.sms.smsCollection.remove({"_id": ObjectId(_id)})

    @gen_test
    def test_report_invalid_request(self):
        number = "9123456789"
        _id = ObjectId()
        data = {
            "number": number,
            "customID": _id,
            "status": "D",
            "datetime": datetime.now().timestamp()
        }
        body = urlencode(data)
        response = yield self.http_client.fetch(self.get_url("/api/report"), method="POST", body=body)
        self.assertEqual(response.code, 200)
        response = json.loads(response.body.decode())
        self.assertEqual(response['status'], 400)



