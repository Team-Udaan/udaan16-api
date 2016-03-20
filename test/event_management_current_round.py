import json

from bson import ObjectId
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import gen_test
from test.base import TestBaseHandler


class CurrentRoundTestHandler(TestBaseHandler):

    @gen_test
    def test_get_current_round_valid_request(self):
        db = self.get_db_client().udaan
        current_round = 0
        event = dict(
            eventName="dummyEvent",
            currentRound=current_round
        )

        event_id = yield db.events.insert(event)
        str_event_id = str(event_id)
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://localhost:8000/api/event_management/current_round", method="GET",
                                           headers=dict(Authorization=str_event_id))
        response_body = json.loads(response.body.decode())
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body["status"], 200)
        self.assertEqual(response_body["message"], str(current_round))

        current_round += 1

        yield db.events.update({"_id": event_id}, {"$inc": {"currentRound": 1}})
        response = yield http_client.fetch("http://localhost:8000/api/event_management/current_round", method="GET",
                                           headers=dict(Authorization=str_event_id))
        response_body = json.loads(response.body.decode())
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body["status"], 200)
        self.assertEqual(response_body["message"], str(current_round))

        yield db.events.remove({"_id": event_id})

    @gen_test
    def test_get_current_round_invalid_request(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://localhost:8000/api/event_management/current_round", method="GET",
                                           headers=None)
        response_body = json.loads(response.body.decode())
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body["status"], 403)
        self.assertEqual(response_body["message"], "Forbidden")

        response = yield http_client.fetch("http://localhost:8000/api/event_management/current_round", method="GET",
                                           headers=dict(Authorization=ObjectId().__str__()))
        response_body = json.loads(response.body.decode())
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body["status"], 401)
        self.assertEqual(response_body["message"], "Invalid Token")
