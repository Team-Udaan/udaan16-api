from urllib import parse

from bson import ObjectId
from tornado.gen import coroutine
from src.base import BaseHandler


class ReportHandler(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):

        """It collects the data and stores the status and datetime in database corresponding to the appropriate customID
        If inserted successfully then a response with status code 200 is sent.
        :param args:
        :param kwargs: """
        
        urlencoded_data = self.request.body.decode()
        str_data = parse.unquote(urlencoded_data)
        data = dict(item.split('=') for item in str_data.split("&"))
        db = self.settings['client'].sms
        document = dict(
                status=data['status'],
                datetime=data['datetime']
        )
        _id = data['customID']
        _id = ObjectId(_id)
        result = yield db.smsCollection.update({"_id": _id}, {"$set": {data["number"]: document}})
        if result["updatedExisting"] is False:
            self.respond("No such number found", 400)
        else:
            self.respond("OK", 200)

    @coroutine
    def get(self, *args, **kwargs):
        """This method will be called when the user wants to see the status of sent messages and a response is sent
        to the user containing all the information regarding the delivery report of appropriate received uid.
        :param kwargs:
        :param args: """
        
        _id = self.get_argument('uid')
        _id = ObjectId(_id)
        db = self.settings['client'].smsCollection
        result = yield db.smsCollection.find_one({"_id": _id})
        if result is None:
            self.respond("Please try again", 400)
        else:
            self.respond(result, 200)
