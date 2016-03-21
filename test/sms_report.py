import json
from datetime import datetime
from urllib.parse import urlencode
from tornado.testing import gen_test
from test.base import TestBaseHandler


class TestReport(TestBaseHandler):
    @gen_test
    def test_report_valid_request(self):
        client = self.get_db_client().udaan
        number = 9123456789
        event_id = yield client.events.insert({"eventName": "Test", "currentRound": 1})
        _id = yield client.participants.insert({"mobileNumber": number, "eventName": "Test", "round1": "q"})
        data = {
            "number": str(910000000000 + number),
            "customID": str(event_id) + "_" + "1",
            "status": "D",
            "datetime": datetime.now().timestamp()
        }
        body = urlencode(data)
        response = yield self.http_client.fetch(self.get_url("/api/report"), method="POST", body=body)
        response = json.loads(response.body.decode())
        self.assertEqual(response['status'], 200)
        yield client.event.remove({"_id": event_id})
        yield client.participants.remove({"_id": _id})

    @gen_test
    def test_report_invalid_request(self):
        client = self.get_db_client().udaan
        number = 9123456789
        event_id = yield client.events.insert({"eventName": "Test", "currentRound": 1})
        _id = yield client.participants.insert({"mobileNumber": number, "eventName": "Test", "round1": "q"})
        data = {
            "number": str(919999999999),
            "customID": str(event_id) + "_" + "1",
            "status": "D",
            "datetime": datetime.now().timestamp()
        }
        body = urlencode(data)
        response = yield self.http_client.fetch(self.get_url("/api/report"), method="POST", body=body)
        response = json.loads(response.body.decode())
        self.assertEqual(response['status'], 400)
        yield client.event.remove({"_id": event_id})
        yield client.participants.remove({"_id": _id})