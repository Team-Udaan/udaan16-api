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
        # TODO
        # 1) Add members to mailing lists
        data = self.get_request_body()
        db = self.settings['client'].subscription
        result = yield db.subscribers.insert({'email': data['email']})
        if result:
            self.add_list_member(data['email'])
            response = 'email-id successfully inserted'
            # TODO
            # 1) create list of status codes in basehandlers.
            status_code = 200
            self.respond(response, status_code)
        else:
            response = 'email-id not inserted'
            status_code = 400
            self.respond(response, status_code)





