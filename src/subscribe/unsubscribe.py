import requests
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from src.base import BaseHandler
from bson.objectid import ObjectId


class UnsubscribeHandler(BaseHandler):
    @coroutine
    def get(self, *args, **kwargs):
        uri = self.request.uri
        temp = "/api/unsubscribe/"
        user_id = uri[len(temp):]
        db = self.settings['client'].subscription
        result = yield db.subscribers.find_one({'email': user_id})
        if result:
            client = AsyncHTTPClient()
            request_object = HTTPRequest("https://api.mailgun.net/v3/lists/list@sandbox1713f24a60034b5ab5e7fa0ca2faa9b6"
                                         ".mailgun.org/members/"+result['email'], method="DELETE", headers=None,
                                         auth_username="api", auth_password="key-a0bd92feef0ccecb07f199b770449917")
            response = yield client.fetch(request_object)
            if response.code == 200:
                result = yield db.subscribers.update({'email': user_id}, {'$set': {'active': False}})
                response = user_id + " is  unsubscribed"
                status_code = 200
                self.respond(response, status_code)
            else:
                response = "Please try again"
                status_code = 400
                self.respond(response, status_code)
        else:
            response = 'user not found in database'
            status_code = 400
            self.respond(response, status_code)
