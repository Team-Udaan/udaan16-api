import json
from urllib import parse
from bson import ObjectId
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from src.base import BaseHandler


class SendSMS(BaseHandler):
    @coroutine
    def post(self, *args, **kwargs):
        
        """->This method will be called when a post request on url-/api/sendsms will be made.
         ->This method will get array of numbers,test,message and it will send the http request to text local API.
         ->The response received from textlocal will be checked and if successful then it will be stored in database
           else a reponse with status code 400 is sent."""
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
            try:
                yield db.smsCollection.insert(document)
                self.respond(sms_id.__str__(), 200)
            except Exception as e:
                self.respond(e.__str__(), 500)
        else:
            response = "unable to send"
            self.respond(response, 400)
