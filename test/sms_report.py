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
        expected_response = dict(
                code=200,
                body=dict(
                        status=200,
                        message="OK"
                )
        )
        body = urlencode(data)
        yield self.check("/api/report", method="POST", headers=None, expected_response=expected_response,
                         body=body)
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
        expexted_response = dict(
                code=200,
                body=dict(
                        status=400,
                        message="No such number found"
                )
        )
        body = urlencode(data)
        self.check("/api/report", method="POST", headers=None,
                   expected_response=expexted_response, body=body)
