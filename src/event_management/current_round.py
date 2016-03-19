from bson import ObjectId
from tornado.gen import coroutine
from src.base import BaseHandler


class CurrentRoundHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        db = self.settings['client'].udaan
        token = self.get_argument('token')
        token = ObjectId(token)
        result = yield db.eventCollection.find_one({"_id": token})
        if result is not None:
            self.respond(str(result['currentRound']), 200)
        else:
            self.respond("token invalid", 401)