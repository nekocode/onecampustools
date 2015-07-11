#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nekocode'

import os
import time
import tornado.ioloop
import tornado.web
import httplib2
import json

class OpenDoorHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    __send_headers = {
        'Host': 'www.uhomecp.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'source': '4',
        'version': '3.2',
        'Connection': 'Keep-Alive',
        'User-Agent': 'uhome_app'
    }

    __login_body = "tel=13246823364&password=110110zxc"

    __opendoor_body = 'communityId=385&doorIdStr='

    __doors_id = {
        "back": "02",
        "5-up": "0550",
        "5-down": "0551"
    }

    def login(self):
        url = 'http://www.uhomecp.com/userInfo/login.json'
        __http = httplib2.Http(timeout=4)
        try:
            response, content = __http.request(url, 'POST', headers=self.__send_headers, body=self.__login_body)
            rlt_json = json.loads(content)
            _rlt = rlt_json['message']
            if not _rlt == u'登录成功':
                return None
            return rlt_json['data']['accessToken']
        except KeyError:
            return None

    def opendoor(self, token, door_str):
        url = 'http://www.uhomecp.com/door/openDoor.json'
        self.__send_headers['token'] = token
        __http = httplib2.Http(timeout=4)
        try:
            response, content = __http.request(url, 'POST', headers=self.__send_headers,
                                               body=self.__opendoor_body + self.__doors_id[door_str])
            rlt_json = json.loads(content)
            _rlt = rlt_json['message']
            if not _rlt == u'成功':
                return False
            return True
        except KeyError:
            return False

    def post(self):
        door_str = self.get_argument("door")
        seconds = int(self.get_argument("delay", "0"))
        if door_str in self.__doors_id:
            time.sleep(seconds)
            token = self.login()
            if token:
                if self.opendoor(token, door_str):
                    self.write('suc')
                else:
                    self.write('failed')
        else:
            self.write('failed')

    def get(self):
        door_str = self.get_argument("door")
        seconds = int(self.get_argument("delay", "0"))
        if door_str in self.__doors_id:
            time.sleep(seconds)
            token = self.login()
            if token:
                if self.opendoor(token, door_str):
                    self.write('suc')
                else:
                    self.write('failed')
        else:
            self.write('failed')

class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.render('index.html')

class MyOpenDoorHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.render('opendoor_mine.html')

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/tools/opendoor_mine", MyOpenDoorHandler),
    (r"/tools/opendoor", OpenDoorHandler)
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


