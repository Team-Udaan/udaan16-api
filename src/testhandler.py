import json

from src.basehandler import BaseHandler


class TestHandler(BaseHandler):

    def post(self, *args, **kwargs):
            response = {}
            response["headers"] = {}
            for header in self.request.headers.get_all():
                temp = dict()
                temp[header[0]] = header[1]
                response['headers'].update(temp)

            response["body"] = self.request.body.decode()
            self.respond(response, 200)


class TestMultipartHandler(BaseHandler):

    def post(self, *args, **kwargs):
        file = self.request.files['image'][0]
        file_name = file["filename"]
        image = file['body']

        with open('images/' + file_name, 'wb+') as f:
            f.write(image)
