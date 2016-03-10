from motor import MotorClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options
from src.subscribe.alert import AlertHandler
from src.subscribe.subscribe import SubscribeHander
from src.subscribe.unsubscribe import UnsubscribeHandler
from src.test import TestHandler, TestMultipartHandler, TestSMSDeliveryHandler

define("port", default=8000, help="run on the given port", type=int)

if __name__ == '__main__':
    client = MotorClient()
    options.parse_command_line()
    app = Application(handlers=[
        (r"/test", TestHandler),
        (r"/subscribe", SubscribeHander),
        (r"/unsubscribe/(.*?)", UnsubscribeHandler),
        (r"/alert", AlertHandler),
        (r"/testsmsdelivery", TestSMSDeliveryHandler),
        (r"/testmultipart", TestMultipartHandler),
        (r"/testmultipart/(.*)", StaticFileHandler, {"path": "images/"})
    ],
        client=client
    )
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.instance().start()
