import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import define, options
from src.testhandler import TestHandler

define("port", default=8000, help="run on given port", type=int)


if __name__ == '__main__':
    options.parse_command_line()
    app = tornado.web.Application(handlers=[
                                           (r"/test", TestHandler)
                                           ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()