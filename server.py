import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options
from src.test import TestHandler, TestMultipartHandler
from src.subscribe.subscribe import SubscribeHander
import motor

define("port", default=8000, help="run on given port", type=int)

client = motor.MotorClient()

if __name__ == '__main__':
    options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/test", TestHandler),
        (r"/testmultipart", TestMultipartHandler),
        (r"/subscribe", SubscribeHander),
        (r"/testmultipart/(.*)", StaticFileHandler, {"path": "images/"})
    ],
        client=client
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
