import json
from urllib import parse
from bson import ObjectId
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from src.base import BaseHandler
from src.event_management.authenticate import authenticate


def get_round_message(round_number, event_name, date, time, venue):
    """

    :param round_number:
    :param event_name:
    :param date:
    :param time:
    :param venue:
    :return:
    """
    message = "Dear Participant, Round " + round_number + " of " + event_name + " is on " + date + " " + time + \
              " at " + venue + ". Kindly be present at the venue on time."
    return message


class SendSMSHandler(BaseHandler):

    @coroutine
    def send_textlocal_sms(self, message, numbers, round_number, test=True):
        """

        :param round_number:
        :param message:
        :param numbers:
        :param test:
        :return:
        """
        data = {
            "username": BaseHandler.environmental_variables["TEXTLOCAL_USERNAME"],
            "hash": BaseHandler.environmental_variables["TEXTLOCAL_HASH"],
            "numbers": numbers,
            "message": message,
            "sender": BaseHandler.environmental_variables["TEXTLOCAL_SENDER"],
            "custom": self.result["_id"].__str__() + "_" + round_number,
            # "custom": str(sms_id),
            'test': test
        }
        request_data = parse.urlencode(data)
        client = AsyncHTTPClient()
        response = yield client.fetch("http://api.textlocal.in/send/", method='POST', headers=None,
                                      body=request_data)
        response = json.loads(response.body.decode())
        return response

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
        # add restriction for max round sms.
        # handle exceptions with transactions

        data = self.parse_request_body()
        teams = data['teams']

        # TODO
        # make default False in production

        test = self.get_json_body_argument("test", default=True)
        numbers = {str(team["mobileNumber"]): "" for team in teams}
        print(numbers)
        numbers_str_list = ','.join(map(str, numbers))
        round_number = str(int(self.result['currentRound']) + 1)
        sms_id = ObjectId()
        message = get_round_message(
            round_number,
            self.result['eventName'],
            self.get_json_body_argument('date'),
            self.get_json_body_argument('time'),
            self.get_json_body_argument('venue')
        )
        response = yield self.send_textlocal_sms(message, numbers_str_list, round_number, test)
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
