import json
from urllib import parse
from bson import ObjectId
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from src.base import BaseHandler

class SendSMS(BaseHandler):
    @coroutine
    def post(self, *args, **kwargs):
        data = self.get_request_body()
        db = self.settings['client'].sms
        msg = data['message']
        numbers = ','.join(map(str, data['numbers']))
        test = data["test"]
        sms_id = ObjectId()
        data = {"username": "anjaras473@gmail.com", "hash": "e2403127a42671bbd3d28192528590589aa52f64",
                "numbers": numbers, "message": msg, "sender": "TXTLCL", "custom": str(sms_id), 'test': test}
        request_data = parse.urlencode(data)
        client = AsyncHTTPClient()
        response = yield client.fetch("http://api.textlocal.in/send/", method='POST', headers=None, body=request_data)
        response = json.loads(response.body.decode())
        print(response)
        if response["status"] == "success":
            document = dict(
                _id=sms_id,
                numbers=numbers,
                message=msg,
                test=test
            )
            result = yield db.smsCollection.insert(document)
            if result is None:
                self.respond("Internal Server error", 500)
            else:
                self.respond(sms_id.__str__(), 200)
        else:
            response = "unable to send"
            self.respond(response, 400)
