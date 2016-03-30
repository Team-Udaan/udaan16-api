import hashlib
from tornado.gen import coroutine
from src.base import BaseHandler


def get_password(email):
    hashed_email = hashlib.sha256(email.encode()).hexdigest()
    hashed_email_6 = hashed_email[:6]
    double_hashed = hashlib.sha256(hashed_email_6.encode()).hexdigest()
    password = double_hashed[:6]
    return password


class LoginHandler(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):

        """This method takes email and password from the request body and matches it with the data stored in database
        If match occurs then a token along with status code 200 is sent else a error code is sent.
        :param kwargs:
        :param args: """

        data = self.parse_request_body()
        db = self.settings['client'].udaan
        email = data['email']
        password = data['password']
        result = yield db.events.find_one({"email": email})
        if result:
            if password == get_password(email):
                token = result['_id']
                token = token.__str__()
                self.respond(token, 200)
            else:
                self.respond("Invalid email id, password combination", 401)
        else:
            self.respond("Invalid email id", 401)
