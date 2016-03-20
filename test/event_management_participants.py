import json

from bson import ObjectId
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import HTTPHeaders
from tornado.testing import gen_test

from test.base import TestBaseHandler


class TestParticipantsHandler(TestBaseHandler):
    @gen_test
    def test_get_participants_valid_request(self):
        db = self.get_db_client().udaan
        event = dict(
                eventName="Test_Get_Participants",
                currentRound=0,
        )
        participant = dict(
                eventName="Test_Get_Participants",
                round0="q",
                _id=str(ObjectId())
        )
        event_insert = yield db.events.insert(event)
        participants_insert = yield db.participants.insert(participant)
        authentication = HTTPHeaders({"Authorization": str(event_insert)})
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(self.get_url("/api/event_management/participants"), method="GET",
                                           headers=authentication)
        response_body = json.loads(response.body.decode())
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body['status'], 200)
        self.assertEqual(response_body['message'][0]["_id"], participant['_id'])
        yield db.events.remove({"_id": event_insert})
        yield db.participants.remove({"_id": participants_insert})

    @gen_test
    def test_get_participants_invalid_request(self):
        authentication = HTTPHeaders({"Authorization": str(ObjectId())})
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(self.get_url("/api/event_management/participants"), method="GET",
                                           headers=authentication)
        response_body = json.loads(response.body.decode())
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body['status'], 401)
        self.assertEqual(response_body['message'], "Invalid Token")

    @gen_test
    def test_post_participants_valid_request(self):
        db = self.get_db_client().udaan

        event = dict(
            eventName="dummyEvent",
            currentRound=0,
        )

        body = dict(
            names="Dummy Names",
            mobileNumber="9123456789"
        )

        request_body = json.dumps(body)

        event_id = yield db.events.insert(event)
        str_event_id = str(event_id)
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://localhost:8000/api/event_management/participants", method="POST",
                                           headers=dict(Authorization=str_event_id), body=request_body)
        response_body = json.loads(response.body.decode())
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body["status"], 200)

        participant = yield db.participants.find_one({"_id": ObjectId(response_body["message"])})
        yield db.participants.remove({"_id": participant["_id"]})
        yield db.events.remove({"_id": event_id})
        self.assertEqual(response_body["message"], participant["_id"].__str__())

    @gen_test()
    def test_post_participants_invalid_request(self):
        db = self.get_db_client().udaan

        event = dict(
            eventName="dummyEvent",
            currentRound=0,
        )

        body = dict(
            names="Dummy Names",
        )

        request_body = json.dumps(body)

        event_id = yield db.events.insert(event)
        str_event_id = str(event_id)
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://localhost:8000/api/event_management/participants", method="POST",
                                           headers=dict(Authorization=str_event_id), body=request_body)
        response_body = json.loads(response.body.decode())
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body["status"], 400)
        self.assertEqual(response_body["message"], "The key mobileNumber is missing in request body")

        yield db.events.remove({"_id": event_id})
