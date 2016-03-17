import hashlib
from bson import ObjectId
from tornado.gen import coroutine

from src.base import BaseHandler


class LoginHandler(BaseHandler):

    def hash(self, email):
        hashed_email = hashlib.sha256(email.encode()).hexdigest()
        hashed_email_6 = hashed_email[:6]
        double_hashed = hashlib.sha256(hashed_email_6.encode()).hexdigest()
        password = double_hashed[:6]
        return password

    @coroutine
    def post(self, *args, **kwargs):
        data = self.get_request_body()
        db = self.settings['client'].udaan
        email = data['email']
        password = data['password']
        result = yield db.eventCollection.find_one({"email": email})
        if result:
            if password == self.hash(email):
                token = result['_id']
                token = token.__str__()
                # TODO
                # insert token into database
                self.respond(token, 200)
            else:
                self.respond("Please try again", 401)
        else:
            self.respond("email-id invalid", 400)
