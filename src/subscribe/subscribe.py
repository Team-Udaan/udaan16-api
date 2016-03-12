import requests
from tornado.gen import coroutine
from src.base import BaseHandler


class SubscribeHander(BaseHandler):
    def add_list_member(self, email_id):
        return requests.post(
            "https://api.mailgun.net/v3/lists/LIST@sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org/members",
            auth=('api', 'key-a0bd92feef0ccecb07f199b770449917'),
            data={'subscribed': True,
                  'address': email_id,
                  'description': 'Subscribers',
                  })

    @coroutine
    def post(self, *args, **kwargs):
        data = self.get_request_body()
        db = self.settings['client'].subscription
        result = yield db.subscribers.find_one({'email': data['email']})
        if result is None:
            response = self.add_list_member(data['email'])
            if response.status_code == 200:
                yield db.subscribers.insert({'email': data['email'], 'active': True})
                msg = 'email-id successfully subscribed'
                # TODO
                # create list of status codes in basehandlers.
                self.respond(msg, response.status_code)
            else:
                msg = 'email-id not subscribed'
                self.respond(msg, response.status_code)
        else:
            msg = 'user already registered'
            status_code = 400
            self.respond(msg, status_code)
