from motor import MotorClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options

from src.base import BaseHandler
from src.sms.report import ReportHandler
from src.sms.sendsms import SendSMS
from src.subscribe.alert import AlertHandler
from src.subscribe.subscribe import SubscribeHander
from src.subscribe.unsubscribe import UnsubscribeHandler
from src.test import TestHandler, TestMultipartHandler, TestSMSDeliveryHandler

define("port", default=8000, help="run on the given port", type=int)


class Handle(BaseHandler):
    def get(self, *args, **kwargs):
        self.respond('OK', 200)

client = MotorClient()


def get_app():
    return Application(handlers=[
        (r"/api/test", TestHandler),
        (r"/api/subscribe", SubscribeHander),
        (r"/api/unsubscribe/(.*?)", UnsubscribeHandler),
        (r"/api/alert", AlertHandler),
        (r"/api/testsmsdelivery", TestSMSDeliveryHandler),
        (r"/api/sendsms",SendSMS),
        (r"/api/report", ReportHandler),
        (r"/api/testmultipart", TestMultipartHandler),
        (r"/api/testmultipart/(.*)", StaticFileHandler, {"path": "images/"}),
        (r"/", Handle)
    ],
        client=client
    )


def get_http_server(application):
    return HTTPServer(application)

if __name__ == '__main__':
    client = MotorClient()
    options.parse_command_line()
    app = get_app()
    http_server = get_http_server(app)
    http_server.listen(options.port)
    IOLoop.current().start()
