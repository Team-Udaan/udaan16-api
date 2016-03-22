
"""This file is the main server file which handles all the http requests and listens on port 8000 by default if nothing
   specified and handles url binding with appropriate RequestHandlers and spawns the IOLoop"""


from motor import MotorClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options

from src.event_management.current_round import CurrentRoundHandler
from src.event_management.login import LoginHandler
from src.base import BaseHandler
from src.events.events import EventsHandler
from src.events.last_modified import LastModifiedHandler
from src.event_management.participants import ParticipantsHandler
from src.sms.report import ReportHandler
from src.sms.sendsms import SendSMSHandler
from src.subscribe.alert import AlertHandler
from src.subscribe.subscribe import SubscribeHander
from src.subscribe.unsubscribe import UnsubscribeHandler
from src.test import TestHandler, TestMultipartHandler, TestSMSDeliveryHandler
from os import environ


define("port", default=8000, help="run on the given port", type=int)

client = MotorClient()


class Handle(BaseHandler):
    def get(self, *args, **kwargs):
        self.respond('OK', 200)


def get_app():
    return Application(handlers=[
        (r"/api/test", TestHandler),
        (r"/api/subscribe", SubscribeHander),
        (r"/api/unsubscribe/(.*?)", UnsubscribeHandler),
        (r"/api/alert", AlertHandler),
        (r"/api/testsmsdelivery", TestSMSDeliveryHandler),
        (r"/api/sendsms", SendSMSHandler),
        (r"/api/report", ReportHandler),
        (r"/api/events", EventsHandler),
        (r"/api/events/lastModified", LastModifiedHandler),
        (r"/api/event_management/login", LoginHandler),
        (r"/api/event_management/participants", ParticipantsHandler),
        (r"/api/event_management/current_round", CurrentRoundHandler),
        (r"/api/testmultipart", TestMultipartHandler),
        (r"/api/testmultipart/(.*)", StaticFileHandler, {"path": "images/"}),
        (r"/", Handle)
    ],
        client=client
    )

port = options.port


def get_http_server(application):
    return HTTPServer(application)

if __name__ == '__main__':

    def check_environment_variables():
        for key in BaseHandler.environmental_variables.keys():
            if key in environ:
                BaseHandler.environmental_variables[key] = environ[key]
                print(BaseHandler.environmental_variables[key])
            else:
                raise SystemExit("Environmental Variables not set")

    check_environment_variables()
    options.parse_command_line()
    app = get_app()
    http_server = get_http_server(app)
    http_server.listen(options.port)
    IOLoop.current().start()