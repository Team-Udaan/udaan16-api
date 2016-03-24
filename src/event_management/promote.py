from bson import ObjectId
from tornado.gen import coroutine

from src.base import BaseHandler
from src.event_management.authenticate import authenticate
from src.event_management.validate import validator
from src.sms.sendsms import get_round_message, send_textlocal_sms


class PromoteHandler(BaseHandler):
    @authenticate
    @coroutine
    def post(self, *args, **kwargs):

        """->This method will be called when a post request on url-/api/sendsms will be made.
         ->This method will get array of numbers,test,message and it will send the http request to text local API.
         ->The response received from textlocal will be checked and if successful then it will be stored in database
           else a reponse with status code 400 is sent.
           :param args:
           :param kwargs: """

        # TODO
        # handle exceptions with transactions
        try:
            if self.result["currentRound"] < 3:
                validate_result = validator(self.parse_request_body())

                if validate_result is True:
                    teams = self.get_json_body_argument("teams")
                    # TODO
                    # make default False in production
                    test = self.get_json_body_argument("test", default=True)
                    numbers = [team["mobileNumber"] for team in teams]
                    numbers_str_list = ','.join(map(str, numbers))
                    round_number = str(int(self.result['currentRound']) + 1)
                    custom = self.result["_id"].__str__() + "_" + round_number
                    sms_id = ObjectId()
                    message = get_round_message(
                        round_number,
                        self.result['eventName'],
                        self.get_json_body_argument('date'),
                        self.get_json_body_argument('time'),
                        self.get_json_body_argument('venue')
                    )

                    response = yield send_textlocal_sms(message, numbers_str_list, round_number, custom, test)
                    if response["status"] == "success":
                        document = dict(
                            _id=sms_id,
                            numbers=numbers,
                            message=message,
                            eventId=self.result["_id"],
                            round=round_number,
                            test=test
                        )
                        try:
                            yield self.db.events.update({"_id": self.result["_id"]}, {"$inc": {"currentRound": 1}})
                            yield self.db.sms.insert(document)
                            for team in teams:
                                yield self.db.participants.update({"_id": ObjectId(team["_id"])},
                                                                  {"$set": {"round" + round_number: "q"}})
                            self.respond(sms_id.__str__(), 200)
                        except Exception as e:
                            self.respond(e.__str__(), 500)
                    else:
                        self.respond(response, 400)
                else:
                    self.respond(validate_result, 400)
            else:
                self.respond("no more round in event", 400)
        except Exception as e:
            self.respond(e.__str__(), 500)
