import tornado
from motor import MotorClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler
from tornado.options import define, options

from src.subscribe.alert import AlertHandler
from src.subscribe.subscribe import SubscribeHander
from src.test import TestHandler, TestMultipartHandler

define("port", default=8000, help="run on the given port", type=int)

if __name__ == '__main__':
    client = MotorClient()
    options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/test", TestHandler),
        (r"/subscribe", SubscribeHander),
        (r"/alert", AlertHandler),
        (r"/testmultipart", TestMultipartHandler),
        (r"/testmultipart/(.*)", StaticFileHandler, {"path": "images/"})
    ],
        client=client
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
