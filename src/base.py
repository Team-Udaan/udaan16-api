from tornado.web import RequestHandler
import json

__author__ = 'alay'


class BaseHandler(RequestHandler):

    environmental_variables = dict(
        TEXTLOCAL_HASH="",
        TEXTLOCAL_SENDER="",
        TEXTLOCAL_USERNAME=""
    )

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
                self.respond("The key " + key + " is missing in request body", 400)
                self.finish()

    def respond(self, response, status_code):

        """This method will be called eveytime a resoponse is to be generated and the parameters passed to it are the
           actual message and the status code for the response and it converts it into a json formatted string and
           sends the appropriate response.
           :param status_code: status code of the response
           :param response: response message of the response object"""

        try:
            _response = {"message": response, "status": status_code}
            data = json.dumps(_response)
            self.write(data)
        except Exception as err:
            self.write(err.__str__())
