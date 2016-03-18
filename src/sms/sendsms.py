import json
from urllib import parse

from bson import ObjectId
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient

from src.base import BaseHandler


class SendSMS(BaseHandler):
    # username =
    # sender =
    # hash =

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
        update = yield db.eventCollection.update({"_id": token}, {"$inc": {"currentRound": 1}})
        numbers = list()
        if result:
            for team in teams:
                participants_result = yield db.participants.update({"mobileNumber": team['mobileNumber']},
                                                                   {"$set": {"round": result['currentRound'],
                                                                             "round" + result['currentRound']: "q"}}
                                                                   )
                numbers.append(participants_result['mobileNumber'])
            round_number = result['currentRound']
            event_name = result['event_name']
            numbers = ','.join(map(str, data['numbers']))
            db = self.settings['client'].sms
            sms_id = ObjectId()
            data = {
                "username": BaseHandler.environmental_variables["TEXTLOCAL_USERNAME"],
                "hash": BaseHandler.environmental_variables["TEXTLOCAL_HASH"],
                "numbers": numbers,
                "message": "Dear Participant, Round " + round_number + " of " + event_name +
                           "is on " + date + " " + time +
                           " at " + venue + ".Kindly be present at the venue on time.",
                "sender": BaseHandler.environmental_variables["TEXTLOCAL_SENDER"],
                "custom": str(sms_id),
                'test': test
            }
            request_data = parse.urlencode(data)
            client = AsyncHTTPClient()
            response = yield client.fetch("http://api.textlocal.in/send/", method='POST', headers=None,
                                          body=request_data)
            response = json.loads(response.body.decode())
            print(response, data)
            if response["status"] == "success":
                document = dict(
                        _id=sms_id,
                        numbers=numbers,
                        message=message,
                        test=test
                )
                try:
                    yield db.smsCollection.insert(document)
                    self.respond(sms_id.__str__(), 200)
                except Exception as e:
                    self.respond(e.__str__(), 500)
            else:
                response = "unable to send"
                self.respond(response, 400)

        else:
            self.respond("token invalid", 401)
