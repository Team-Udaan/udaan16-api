from urllib.parse import urlencode
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from src.base import BaseHandler


class AlertHandler(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):
        # TODO
        # save the messages to local database
        file = self.request.files['image'][0]
        file_name = file["filename"]
        image = file['body']
        text = self.get_argument("text")
        data={
                "from": "Mailgun Sandbox <postmaster@sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org>",
                "to": "<list@sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org>",
                "subject": "Hello Udaan",
                "text": text,
                "inline": image,
                }
        data = urlencode(data)
        client = AsyncHTTPClient()
        request_object = HTTPRequest("https://api.mailgun.net/v3/sandbox1713f24a60034b5ab5e7fa0ca2faa9b6.mailgun.org"
                                     "/messages", method="POST", headers=None, body=data,auth_username="api",
                                     auth_password="key-a0bd92feef0ccecb07f199b770449917")
        response = yield client.fetch(request_object)
        client.close()
        if response.code == 200:
            msg = "email send successfully"
            self.respond(msg, response.code)
        else:
            msg = "Please try again"
            self.respond(msg, response.code)
