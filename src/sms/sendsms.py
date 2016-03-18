import json
from urllib import parse
from bson import ObjectId
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from src.base import BaseHandler


class SendSMSHandler(BaseHandler):
    # username =
    # sender =
    # hash =

    def get_message(self, round_number, event_name, date, time, venue):
        message = "Dear Participant, Round " + round_number + " of " + event_name + "is on " + date + " " + time + \
                  " at " + venue + ".Kindly be present at the venue on time."
        return message

    def send_textlocal_sms(self, message, numbers, sms_id, test=True):
        data = {
            "username": BaseHandler.environmental_variables["TEXTLOCAL_USERNAME"],
            "hash": BaseHandler.environmental_variables["TEXTLOCAL_HASH"],
            "numbers": numbers,
            "message": message,
            "sender": BaseHandler.environmental_variables["TEXTLOCAL_SENDER"],
            "custom": str(sms_id),
            'test': test
        }
        request_data = parse.urlencode(data)
        client = AsyncHTTPClient()
        response = yield client.fetch("http://api.textlocal.in/send/", method='POST', headers=None,
                                      body=request_data)
        response = json.loads(response.body.decode())
        return response

    @coroutine
    def post(self, *args, **kwargs):

        """->This method will be called when a post request on url-/api/sendsms will be made.
         ->This method will get array of numbers,test,message and it will send the http request to text local API.
         ->The response received from textlocal will be checked and if successful then it will be stored in database
           else a reponse with status code 400 is sent.
           :param args:
           :param kwargs: """
        db = self.settings['client'].udaan
        data = self.get_request_body()
        token = data['token']
        teams = data['teams']
        message = data['message']
        date = data['date']
        time = data['time']
        venue = data['venue']
        test = data['test']
        token = ObjectId(token)

        result = yield db.eventCollection.find_one({"_id": token})
        numbers = list()
        if result is not None:
            for team in teams:
                yield db.participants.find_one({"_id": ObjectId(team['id'])})
                numbers.append(team['mobileNumber'])
            yield db.eventCollection.update({"_id": result["_id"]}, {"$inc": {"currentRound": 1}})
            result = yield db.eventCollection.find_one({"_id": token})
            round_number = str(result['roundNumber'])
            event_name = result['event_name']
            numbers = ','.join(map(str, data['numbers']))
            db = self.settings['client'].sms
            sms_id = ObjectId()
            response = self.send_textlocal_sms(self.get_message(round_number, event_name, date, time, venue),
                                               numbers, sms_id)
            if response["status"] == "success":
                document = dict(
                        _id=sms_id,
                        numbers=numbers,
                        message=message,
                        test=test
                )
                try:
                    yield db.smsCollection.insert(document)
                    db = self.settings['client'].udaan
                    for team in teams:
                        yield db.participants.update({"mobileNumber": team['mobileNumber']},
                                                     {"$set": {"round" + round_number: "q"}})
                    self.respond(sms_id.__str__(), 200)
                except Exception as e:
                    self.respond(e.__str__(), 500)
            else:
                response = "unable to send"
                self.respond(response, 400)

        else:
            self.respond("token invalid", 401)
