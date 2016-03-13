from datetime import datetime
import json
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
        client = AsyncHTTPClient()
        response = yield client.fetch("http://msg.yeshasoftware.com/api/sendhttp.php?authkey=10285ArwR3m6OoWte56e11baa"
                                      "&mobiles=" + numbers + "&message=" + msg + "&sender=YSDEMO&route=4&"
                                      "country=91&response=json", method='GET', headers=None)
        response = json.loads(response.body.decode())
        _id = ObjectId(response['message'])
        if response["type"] == "success":
            document = dict(
                    _id=_id,
                    numbers=numbers,
                    message=msg,
                    timestamp=datetime.now()
            )
            try:
                yield db.smsCollectionYesha.insert(document)
                self.respond(_id.__str__(), 200)
            except Exception as e:
                self.respond(e.__str__(), 500)
        else:
            response = "unable to send"
            self.respond(response, 400)
