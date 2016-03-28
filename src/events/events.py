from tornado.gen import coroutine

from src.base import BaseHandler


class EventsHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):

        """This method will send the entire data regarding all the events."""

        db = self.settings["client"].udaan
        result = yield db.varunFormattedEvents.find_one()
        del result["_id"]
        del result["lastModified"]
        self.respond(result, 200)
