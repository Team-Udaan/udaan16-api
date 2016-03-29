from tornado.gen import coroutine
from src.base import BaseHandler


class LastModifiedHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):

        """This method will check if the data is modified or not if the data is not modified then the data will not be
        sent."""
        
        db = self.settings["client"].udaan
        result = yield db.varunFormattedEvents.find_one({}, {"lastModified": 1})
        self.respond(str(result["lastModified"].timestamp()), 200)
        # self.respond(result, 200)
