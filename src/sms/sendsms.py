import json
from urllib import parse
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from src.base import BaseHandler


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


@coroutine
def send_textlocal_sms(message, numbers, round_number, custom=None, test=True):
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
        "custom": custom,
        'test': test
    }
    request_data = parse.urlencode(data)
    client = AsyncHTTPClient()
    response = yield client.fetch("http://api.textlocal.in/send/", method='POST', headers=None,
                                  body=request_data)
    response = json.loads(response.body.decode())
    return response
