import requests
from tornado.gen import coroutine
from src.base import BaseHandler
from bson.objectid import ObjectId


def remove_member(email):
    return requests.delete(
        (
            "https://api.mailgun.net/v3/lists/list@sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org/members/"
            + email),
        auth=('api', 'key-a0bd92feef0ccecb07f199b770449917'))


class UnsubscribeHandler(BaseHandler):
    @coroutine
    def get(self, *args, **kwargs):
        uri = self.request.uri
        temp = "/unsubscribe/"
        user_id = uri[len(temp):]
        _id = ObjectId(user_id)
        db = self.settings['client'].subscription
        result = yield db.subscribers.find_one({'_id': _id})
        if result:
            response = remove_member(result['email'])
            if response.status_code == 200:
                result = yield db.subscribers.update({'email': result['email']}, {'active': False})
                response = result['email'] + " is  unsubscribed"
                status_code = 200
                self.respond(response, status_code)
            else:
                response = "Please try again"
                status_code = 400
                self.respond(response, status_code)
        else:
            response = 'user not found in database'
            status_code = 400
            self.respond(response, status_code)
