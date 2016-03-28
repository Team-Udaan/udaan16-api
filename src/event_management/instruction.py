from tornado.gen import coroutine

from src.base import BaseHandler


class InstructionHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        db = self.settings["client"].udaan
        result = yield db.instrunctions.find_one()
        if result is not None:
            self.respond(result['instruction'], 200)
        else:
            self.respond("instructions not found", 400)
