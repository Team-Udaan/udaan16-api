import json
from tornado.testing import gen_test
from test.base import TestBaseHandler
from hashlib import sha256


class LoginTestHandler(TestBaseHandler):

    @gen_test
    def test_login_valid_request(self):
        # db = self.get_db_client().udaan
        email = "janitirth17110@gmail.com"
        password = sha256(sha256(email.encode()).hexdigest()[0:6].encode()).hexdigest()[0:6]
        # password = '2b615c'
        data = dict(
            email=email,
            password=password
        )
        document = yield self.get_db_client().udaan.events.find_one({"email": email})
        expected_response = dict(
            code=200,
            body=dict(
                status=200,
                message=str(document["_id"])

            )
        )
        body = json.dumps(data)
        yield self.check("/api/event_management/login", method="POST", headers= None,
                         expected_response=expected_response, body=body)

    @gen_test
    def test_login_invalid_request(self):
        invalid_email = "invalid@email.com"
        invalid_email_password = "doesnt matter"

        valid_email = "janitirth17110@gmail.com"
        valid_email_invalid_password = "invalid"

        invalid_email_data = dict(
            email=invalid_email,
            password=invalid_email_password
        )
        expected_response_invalid_email = dict(
            code=200,
            body=dict(
                status=401,
                message="Invalid email id"
            )
        )
        body = json.dumps(invalid_email_data)
        yield self.check("/api/event_management/login", method="POST", headers=None,
                         expected_response=expected_response_invalid_email, body=body)

        valid_email = dict(
            email=valid_email,
            password=valid_email_invalid_password
        )
        expected_response_valid_email = dict(
            code=200,
            body=dict(
                status=401,
                message="Invalid email id, password combination"
            )
        )
        body = json.dumps(valid_email)
        yield self.check("/api/event_management/login", method="POST", headers=None,
                         expected_response=expected_response_valid_email, body=body)

