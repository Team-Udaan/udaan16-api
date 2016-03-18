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
        token = ObjectId(token)
        result = yield db.eventCollection.find_one({"_id": token})
        try:
            round_number = str(parameters['round'])
            if round_number == "current":
                round_number = str(result["currentRound"])
        except KeyError as e:
            round_number = str(result["currentRound"])
        message = list()
        if result is not None:
            participants = db.participants.find({"round" + round_number: "q"},
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
        name = data['names']
        mobile_number = data['mobileNumber']
        token = data['token']
        token = ObjectId(token)
        document = dict(
            names=name,
            mobileNumber=mobile_number,
            round0="NA",
            round1="NA",
            round2="NA",
            round3="NA",
        )
        result = yield db.eventCollection.find_one({"_id": token})
        if result is not None:
            current_round = result['currentRound']
            inserted = yield db.participants.insert(document)
            for i in range(0, current_round + 1):
                yield db.participants.update({"_id": inserted},
                                            {"$set": {"round" + str(i): "q"}})
        else:
            self.respond("invalid token", 401)
