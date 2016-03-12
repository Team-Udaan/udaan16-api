from motor import MotorClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options

from src.sms.report import ReportHandler
from src.sms.sendsms import SendSMS

from src.subscribe.alert import AlertHandler
from src.subscribe.subscribe import SubscribeHander
from src.subscribe.unsubscribe import UnsubscribeHandler
from src.test import TestHandler, TestMultipartHandler, TestSMSDeliveryHandler

define("port", default=8000, help="run on the given port", type=int)

if __name__ == '__main__':
    client = MotorClient()
    options.parse_command_line()
    app = Application(handlers=[
        (r"/api/test", TestHandler),
        (r"/api/subscribe", SubscribeHander),
        (r"/api/unsubscribe/(.*?)", UnsubscribeHandler),
        (r"/api/alert", AlertHandler),
        (r"/api/testsmsdelivery", TestSMSDeliveryHandler),
        (r"/api/sendsms",SendSMS),
        (r"/api/report", ReportHandler),
        (r"/api/testmultipart", TestMultipartHandler),
        (r"/api/testmultipart/(.*)", StaticFileHandler, {"path": "images/"})
    ],
        client=client
    )
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.instance().start()
