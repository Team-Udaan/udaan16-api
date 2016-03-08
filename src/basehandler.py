from tornado.web import RequestHandler
import json

__author__ = 'alay'


class BaseHandler(RequestHandler):

    def initialize(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "false")
        self.set_header("Access-Control-Expose-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "*")
        self.set_header("Access-Control-Allow-Headers", "*")

    def options(self, *args, **kwargs):
        self.send_error(200)

    def respond(self, response, status_code):
        try:
            _response = {}
            _response["message"] = response
            _response["status"] = status_code
            self.write(json.dumps(_response))
        except Exception as err:
            self.write(err)