from tornado.gen import coroutine
from src.base import BaseHandler
from src.event_management.authenticate import authenticate


class CurrentRoundHandler(BaseHandler):

    @authenticate
    @coroutine
    def get(self, *args, **kwargs):
        self.respond(str(int(self.result["currentRound"])), 200)

