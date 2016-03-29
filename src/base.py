import json
import traceback
from datetime import datetime
from tornado.gen import coroutine
from tornado.web import RequestHandler

__author__ = 'alay'


class BaseHandler(RequestHandler):

    environmental_variables = dict(
        TEXTLOCAL_HASH="",
        TEXTLOCAL_SENDER="",
        TEXTLOCAL_USERNAME=""
    )

    @coroutine
    def prepare(self):
        self.start_time = datetime.now().timestamp()
        request = dict(self.request.__dict__.items())
        headers = dict(self.request.headers.__dict__.items())
        request = dict(
            uri=request["uri"],
            body=request["body"],
            headers=headers["_dict"]
        )
        self.log_id = yield self.db.logger.insert({"request": request})

    def initialize(self):

        """It will set the given response headers"""

        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "false")
        self.set_header("Access-Control-Expose-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.body = dict()
        self._parsed = False
        self.result = dict()
        self.db = self.settings["client"].udaan
        self.log_id = None
        self._response = None

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an ``exc_info`` triple will be available as
        ``kwargs["exc_info"]``.  Note that this exception may not be
        the "current" exception for purposes of methods like
        ``sys.exc_info()`` or ``traceback.format_exc``.
        :param status_code:
        """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.set_header('Content-Type', 'application/json')
            self.set_header("Access-Control-Allow-Origin", "*")
            # self.set_header("Access-Control-Allow-Credentials", "false")
            self.set_header("Access-Control-Expose-Headers", "*")
            self.set_header("Access-Control-Allow-Methods", "*")
            self.set_header("Access-Control-Allow-Headers", "accept, authorization")
            self._status_code = 200
            data = json.dumps(dict(
                code=status_code,
                message=kwargs.get("exc_info").__str__()
            ))
            self.finish(data)

    def set_result(self, result):
        self.result = result

    def options(self, *args, **kwargs):
        self.send_error(200)

    def parse_request_body(self):

        """It will convert the request body data into dictionary data and if an exception
           occurs then a response with status code 500 is sent."""

        try:
            if self._parsed is False:
                self.body = json.loads(self.request.body.decode())
                self._parsed = True
            return self.body
        except Exception as e:
            self.respond(str(e), 500)

    def get_json_body_argument(self, key, default=None):
        # TODO
        # Document it.
        try:
            if self._parsed is False:
                self.body = self.parse_request_body()
            return self.body[key]
        except KeyError:
            if default is not None:
                return default
            else:
                raise Exception("The key " + key + " is missing in request body")

    def respond(self, response, status_code):

        """This method will be called eveytime a resoponse is to be generated and the parameters passed to it are the
           actual message and the status code for the response and it converts it into a json formatted string and
           sends the appropriate response.
           :param status_code: status code of the response
           :param response: response message of the response object"""

        try:
            self._response = {"message": response, "status": status_code}
            data = json.dumps(self._response)
            self.write(data)
        except Exception as err:
            self.write(err.__str__())

    @coroutine
    def on_finish(self):
        end_time = datetime.now().timestamp()
        serve_time = end_time - self.start_time
        yield self.db.logger.update({"_id": self.log_id},
                                    {"$set": {"response": self._response,
                                              "serveTime": serve_time,
                                              "request.body": self.body
                                              }})
