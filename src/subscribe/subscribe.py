from tornado.gen import coroutine
from src.base import BaseHandler


class SubscribeHander(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):
        # TODO
        # 1) Add members to mailing lists
        data = self.get_request_body()
        db = self.settings['client'].subscription
        result = yield db.subscribers.insert({'email': data['email']})
        if result:
            response = 'email-id successfully inserted'
            # TODO
            # 1) create list of status codes in basehandlers.
            status_code = 200
            self.respond(response, status_code)
        else:
            response = 'email-id not inserted'
            status_code = 400
            self.respond(response, status_code)




