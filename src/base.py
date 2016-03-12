from tornado.web import RequestHandler
import json

__author__ = 'alay'


class BaseHandler(RequestHandler):

    def initialize(self):
        
        """It will set the given response headers"""
        
        self.set_header('Content-Type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "false")
        self.set_header("Access-Control-Expose-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "*")
        self.set_header("Access-Control-Allow-Headers", "*")

    def options(self, *args, **kwargs):
        self.send_error(200)

    def get_request_body(self):
        
        """It will be called everytime a request body is to be converted into dictionary data.
           It will convert the given request body data into dictionary data and if an exception 
           occurs then a response with status code 500 is sent."""
        
        try:
            return json.loads(self.request.body.decode())
        except Exception as e:
            self.respond(str(e), 500)

    def respond(self, response, status_code):
        
        """This method will be called eveytime a resoponse is to be generated and the parameters passed to it are the
           actual message and the status code for the response and it converts it into a json formatted string and
           sends the appropriate response."""

        
        try:
            _response = {"message": response, "status": status_code}
            data = json.dumps(_response)
            self.write(data)
        except Exception as err:
            self.write(err)
