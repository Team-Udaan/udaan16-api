from tornado.gen import coroutine
from src.base import BaseHandler


class InstructionsHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        db = self.settings["client"].udaan
        result = yield db.instructions.find_one()
        if result is not None:
            self.respond(result['instruction'], 200)
        else:
            self.respond("instructions not found", 400)
