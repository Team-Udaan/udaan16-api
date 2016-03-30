from urllib import parse
from urllib.parse import parse_qsl
from tornado.gen import coroutine
from src.base import BaseHandler
from src.event_management.authenticate import authenticate


class ParticipantsHandler(BaseHandler):

    @authenticate
    @coroutine
    def get(self, *args, **kwargs):

        """This method will send the list of participants to the manager based on the data sent in request url, if the
           token is not found in database then a error message is sent.
           :param kwargs:
           :param args: """

        # TODO
        # add receiptId to the parameters
        # remove count and setting of participants["receiptId"] in production

        url = self.request.uri
        unquoted_url = parse.unquote(url)
        parsed_url = parse.urlparse(unquoted_url)
        parameters = parse_qsl(parsed_url.query)
        parameters = dict(parameters)
        try:
            round_number = str(parameters['round'])
            if round_number == "current":
                round_number = str(int(self.result["currentRound"]))
        except KeyError as e:
            round_number = str(int(self.result["currentRound"]))
        participants = list()
        if int(round_number) > self.result['currentRound']:
            self.respond("No such round found", 400)
        else:
            participants_cursor = self.db.participants.find({"round" + round_number: "q",
                                                            "eventName": self.result["eventName"]},
                                                            {"_id": 1, "names": 1, "mobileNumber": 1,
                                                             "smsStatus": 1, "receiptId": 1})
            while (yield participants_cursor.fetch_next):
                participant = participants_cursor.next_object()
                participant["_id"] = str(participant["_id"])
                if "smsStatus" in participant:
                    participant["smsStatus"] = participant["smsStatus"]["status"]
                else:
                    participant.setdefault("smsStatus", "NA")
                participants.append(participant)
            message = dict(
                participants=participants,
                eventName=self.result["eventName"]
            )
            self.respond(message, 200)

    @authenticate
    @coroutine
    def post(self, *args, **kwargs):

        """This method will receive the data from the manager to add on the sport participants entry
        and appropriately make change in the database and also update the corresponding rounds
        :param kwargs:
        :param args: """
        if self.result["currentRound"] == self.get_json_body_argument("currentRound"):
            try:
                document = dict(
                    names=self.get_json_body_argument("names"),
                    mobileNumber=self.get_json_body_argument("mobileNumber"),
                    eventName=self.result["eventName"],
                    round0="NA",
                    round1="NA",
                    round2="NA",
                    round3="NA",
                )
                current_round = int(self.result['currentRound'])
                for i in range(0, current_round + 1):
                    document["round"+str(i)] = "q"
                inserted = yield self.db.participants.insert(document)
                if inserted is not None:
                    self.respond(str(inserted), 200)
            except Exception as i:
                self.respond(i.__str__(), 500)
        else:
            self.respond("current round not matched", 400)
