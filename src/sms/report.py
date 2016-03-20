from urllib import parse
from bson import ObjectId
from tornado.gen import coroutine
from src.base import BaseHandler
from src.event_management.authenticate import authenticate


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
        custom_id_list = str(data['customID']).split("_")
        str_id, round_number = custom_id_list[0], custom_id_list[1]
        _id = ObjectId(str_id)
        # TODO
        # remove this in production
        number = str(data['number'])[-10:]
        del data["number"], data["customID"]
        self.result = yield self.db.events.find_one({"_id": _id})
        result = yield self.db.participants.update({"eventName": self.result["eventName"], "round" + round_number: "q",
                                                    "mobileNumber": int(number)}, {"$set": {"smsStatus": data}})
        if result["updatedExisting"] is False:
            self.respond("No such number found", 400)
        else:
            self.respond("OK", 200)

    @authenticate
    @coroutine
    def get(self, *args, **kwargs):
        """This method will be called when the user wants to see the status of sent messages and a response is sent
        to the user containing all the information regarding the delivery report of appropriate received uid.
        :param kwargs:
        :param args: """

        current_round = str(int(self.result["currentRound"]))
        result = yield self.db.sms.find_one({"eventId": self.result["_id"], "round": current_round})
        if result is None:
            self.respond("Please try again", 400)
        else:
            self.respond(result, 200)
