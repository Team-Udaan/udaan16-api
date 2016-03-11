import json
import urllib

from src.base import BaseHandler


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


class TestSMSDeliveryHandler(BaseHandler):

    def serve(self):
        print(self.request)
        with open("record.txt", "a+") as f:
            f.write(str(self.request) + "\n")
        self.respond("working", 200)

    def get(self, *args, **kwargs):
        self.serve()
        # response = {}
        # data = self._get_arguments("data", self.request.arguments)
        # response["data"] = json.loads(data[0])
        # response["headers"] = {}
        # for header in self.request.headers.get_all():
        #     temp = dict()
        #     temp[header[0]] = header[1]
        #     response['headers'].update(temp)
        #
        # response["body"] = self.request.body.decode()
        # print(response)
        # self.respond(response, 200)

    def post(self, *args, **kwargs):
        self.serve()
