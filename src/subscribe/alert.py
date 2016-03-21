from json import dumps
from urllib.parse import urlencode

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httputil import HTTPHeaders

from src.base import BaseHandler


class AlertHandler(BaseHandler):
    @coroutine
    def post(self, *args, **kwargs):
        # TODO
        # save the messages to local database
        # file = self.request.files['image'][0]
        # file_name = file["filename"]
        # image = file['body']
        text = self.get_argument("text")
        data = {
            "from": "Mailgun Sandbox <postmaster@sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org>",
            "to": "<list@sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org>",
            "subject": "Hello Udaan",
            "text": text,
        }
        data = urlencode(data)
        client = AsyncHTTPClient()
        headers_object = HTTPHeaders({"X-Mailgun-Variables": dumps({"X-Mailgun-Variables": {"password": "working"}})})
        request_object = HTTPRequest("https://api.mailgun.net/v3/sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org"
                                     "/messages",
                                     method="POST",
                                     headers=headers_object,
                                     body=data,
                                     auth_username="api",
                                     auth_password="key-a0bd92feef0ccecb07f199b770449917"
                                     )
        print(request_object.headers.get_list("X-Mailgun-Variables"))
        response = yield client.fetch(request_object)
        client.close()
        print(response)
        if response.code == 200:
            msg = "email send successfully"
            self.respond(msg, response.code)
        else:
            msg = "Please try again"
            self.respond(msg, response.code)
