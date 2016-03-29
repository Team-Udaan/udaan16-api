from functools import wraps
from bson import ObjectId
from tornado.gen import coroutine


def authenticate(function):

    """This function is for the decorator @authenticate, all the users logging in would be verified with the database
    entries if not found then they a error will be sent."""

    @coroutine
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        token = self.request.headers.get("Authorization")
        if token is None:
            self.respond("Forbidden", 403)
        else:
            try:
                _id = ObjectId(token)
                result = yield self.db.events.find_one({"_id": _id})
                self.set_result(result)
                if self.result is not None:
                    yield function(self, *args, **kwargs)
                else:
                    self.respond("Invalid Token", 401)
            except Exception as i:
                self.respond(str(i), 400)
    return wrapper
