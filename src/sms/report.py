from bson import ObjectId
from tornado.gen import coroutine
from src.base import BaseHandler


class ReportHandler(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):
        data = self.get_request_body()
        db = self.settings['client'].smsCollection
        document = dict(
                status=data['status'],
                datetime=data['datetime']
        )
        _id = data['customID']
        _id = ObjectId(_id)
        result = yield db.smsCollection.update({"_id": _id}, {"$set": {data["number"]: document}})
        if result is None:
            self.write_error(400)
        else:
            self.respond("OK", 200)

    @coroutine
    def get(self, *args, **kwargs):
        _id = self.get_argument('uid')
        _id = ObjectId(_id)
        db = self.settings['client'].smsCollection
        result = yield db.smsCollection.find_one({"_id":_id})
        if result is None:
            self.respond("Please try again",400)
        else:
            self.respond(result, 200)
