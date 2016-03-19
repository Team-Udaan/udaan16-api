from functools import wraps

from bson import ObjectId
from bson.errors import InvalidId
from tornado.gen import coroutine


def authenticate(function):
    @coroutine
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        token = self.request.headers.get("Authorization")
        try:
            _id = ObjectId(token)
            result = yield self.db.events.find_one({"_id": _id})
            self.set_result(result)
            if self.result is not None:
                yield function(self, *args, **kwargs)
            else:
                self.respond("Invalid Token", 401)
        except InvalidId as i:
            self.respond(str(i), 400)
    return wrapper
