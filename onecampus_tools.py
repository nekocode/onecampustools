#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nekocode'

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
        'version': '3.1',
        'Connection': 'Keep-Alive',
        'User-Agent': 'uhome_app'
    }

    __login_body = "tel=13246823364&password=110110zxc"

    __opendoor_body = 'communityId=385&doorIdStr=0551'

    def login(self):
        url = 'http://www.uhomecp.com/userInfo/login.json'
        __http = httplib2.Http()
        response, content = __http.request(url, 'POST', headers=self.__send_headers, body=self.__login_body)
        rlt_json = json.loads(content)
        try:
            _rlt = rlt_json['message']
            if not _rlt == u'登录成功':
                return None
            _rlt = rlt_json['data']['accessToken']
        except KeyError:
            _rlt = None
        return _rlt

    def opendoor(self, token):
        url = 'http://www.uhomecp.com/door/openDoor.json'
        self.__send_headers['token'] = token
        __http = httplib2.Http()
        response, content = __http.request(url, 'POST', headers=self.__send_headers, body=self.__opendoor_body)
        rlt_json = json.loads(content)
        try:
            _rlt = rlt_json['message']
            if not _rlt == u'成功':
                return False
            _rlt = True
        except KeyError:
            _rlt = False
        return _rlt

    def get(self):
        self.write('<html><body><form action="/" method="post">'
                   '<input type="submit" value="打开后门~">'
                   '</form></body></html>')

    def post(self):
        token = self.login()
        if token:
            if self.opendoor(token):
                self.write('开门成功 o(≧口≦)o ')
            else:
                self.write('好像出了点问题 ╮(╯▽╰)╭\n你可以尝试联系开发者 wechat: nekocode')


application = tornado.web.Application([
    (r"/tools/open_door", OpenDoorHandler)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
