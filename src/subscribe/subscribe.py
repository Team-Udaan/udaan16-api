from urllib.parse import urlencode

import requests
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from src.base import BaseHandler


class SubscribeHander(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):
        data = self.get_request_body()
        db = self.settings['client'].subscription
        email = data['email']
        result = yield db.subscribers.find_one({'email': email})
        if result is None:
            data = {'subscribed': True,
                    'address': email,
                    'description': 'Subscribers',
                   }
            data = urlencode(data)
            client = AsyncHTTPClient()
            request_object = HTTPRequest("https://api.mailgun.net/v3/lists/LIST@sandbox1713f24a60034b5ab5e7fa0ca2faa9b"
                                         "6.mailgun.org/members", method="POST", headers=None, body=data, auth_username=
                                         "api", auth_password="key-a0bd92feef0ccecb07f199b770449917")
            response = yield client.fetch(request_object)
            if response.code == 200:
                yield db.subscribers.insert({'email': email, 'active': True})
                msg = 'email-id successfully subscribed'
                # TODO
                # create list of status codes in basehandlers.
                self.respond(msg, response.code)
            else:
                msg = 'email-id not subscribed'
                self.respond(msg, response.code)
        else:
            msg = 'user already registered'
            status_code = 400
            self.respond(msg, status_code)




