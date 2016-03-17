from tornado.gen import coroutine

from src.base import BaseHandler


class EventsHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        db = self.settings["client"].udaan
        result = yield db.varunFormattedEvents.find_one()
        del result["_id"]
        self.respond(result, 200)
