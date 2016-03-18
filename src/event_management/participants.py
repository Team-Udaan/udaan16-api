from urllib import parse
from urllib.parse import parse_qsl
from bson import ObjectId
from tornado.gen import coroutine
from src.base import BaseHandler


class ParticipantsHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        db = self.settings['client'].udaan
        url = self.request.uri
        unquoted_url = parse.unquote(url)
        parsed_url = parse.urlparse(unquoted_url)
        parameters = parse_qsl(parsed_url.query)
        parameters = dict(parameters)
        token = parameters['token']
        round_number = parameters['round']
        token = ObjectId(token)
        result = yield db.eventCollection.find_one({"_id": token})
        message = list()
        if result is not None:
            if round_number == "current":
                participants = db.paricipants.find({"round" + result['currentRound']: "q"},
                                                   {"_id": 1, "names": 1, "mobileNumber": 1})
                while (yield participants.fetch_next):
                    document = participants.next_object()
                    message.append(document)
                self.respond(message, 200)
            else:
                participants = db.paricipants.find({"round" + round_number: "q"},
                                                   {"_id": 1, "names": 1, "mobileNumber": 1})
                while (yield participants.fetch_next):
                    document = participants.next_object()
                    message.append(document)
                self.respond(message, 200)
        else:
            self.respond("token invalid", 401)

    @coroutine
    def post(self, *args, **kwargs):
        data = self.get_request_body()
        db = self.settings['client'].udaan
        username = data['username']
        mobile_number = data['mobileNumber']
        token = data['token']
        round_number = data['round']
        token = ObjectId(token)
        result = yield db.eventCollection.find_one({"_id": token})
        if result is not None:
            if round == 1:
                document = dict(
                        name=username,
                        mobileNumber=mobile_number,
                        round=result['currentRound'],
                        round1="q",
                        round2="n/a",
                        round3="n/a",
                )
            if round_number == 2:
                document = dict(
                        name=username,
                        mobileNumber=mobile_number,
                        round=result['currentRound'],
                        round1="q",
                        round2="q",
                        round3="n/a",
                )
            insert_result = db.paricipants.insert(document)
            if insert_result:
                self.respond(insert_result.__str__(), 200)
            else:
                self.respond("enable to insert", 400)
        else:
            self.respond("token invalid", 401)
