import json
from tornado.httpclient import AsyncHTTPClient
from tornado.testing import gen_test
from test.base import TestBaseHandler
from hashlib import sha256


class LoginTestHandler(TestBaseHandler):

    @gen_test
    def test_login_valid_request(self):
        email = "janitirth17110@gmail.com"
        password = sha256(sha256(email.encode()).hexdigest()[0:6].encode()).hexdigest()[0:6]
        data = dict(
            email=email,
            password=password
        )
        body = json.dumps(data)
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://localhost:8000/api/event_management/login", method='POST', headers=None, body=body)
        response_body = json.loads(response.body.decode())
        self.assertEqual(response.code, 200)
        self.assertEqual(response_body["status"], 200)
        document = yield self.get_db_client().udaan.eventCollection.find_one({"email": email})
        self.assertEqual(response_body["message"], str(document["_id"]))