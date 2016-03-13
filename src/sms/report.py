import json
from bson import ObjectId
from tornado.gen import coroutine
from src.base import BaseHandler


class ReportHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        response = {}
        data = self._get_arguments("data", self.request.arguments)
        response["data"] = json.loads(data[0])
        db = self.settings['client'].sms
        document = dict(
                status=data['status'],
                datetime=data['date']
        )
        _id = response["data"]["reqid"]
        _id = ObjectId(_id)
        try:
            yield db.smsCollectionYesha.update({"_id": _id}, {"$set": {"logs": {data["number"]: document}}})
            self.respond(_id.__str__(), 200)
        except Exception as e:
            self.respond(e.__str__(), 500)


    @coroutine
    def post(self, *args, **kwargs):
        data = self.get_request_body()
        db = self.settings['client'].sms
        _id = data['_id']
        _id = ObjectId(_id)
        try:
            result = yield db.smsCollectionYesha.find_one({"_id":_id})
            result['_id'] = result['_id'].__str__()
            self.respond(result, 200)
        except Exception as e:
            self.respond(e.__str__(), 500)
