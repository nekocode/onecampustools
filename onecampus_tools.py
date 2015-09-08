#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import tornado.ioloop
import tornado.web
import httplib2
import json
import bus_check
__author__ = 'nekocode'


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


class CheckBusHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        # self.write('<meta name="viewport" content="width=device-width, initial-scale=1"/>')
        self.write('<title>公交查询</title><style>body{background:#22292C;color:#fff}</style>')
        hour = int(time.strftime('%H', time.localtime()))
        if hour < 13:
        	self.write('<table cellpadding="10" width="100%" onclick="location.reload()"><tr><th>大学城专线 1(去上班)</th><th>大学城专线 2(去上班)</th></tr>')
        else:
            self.write('<table cellpadding="10" width="100%" onclick="location.reload()"><tr><th>大学城专线 1(回家)</th><th>大学城专线 2(回家)</th></tr>')

        bus_data = bus_check.get_bus_data()
        bus_img = '<img src="/static/img/bus.svg"/>'
        for i in range(max(len(bus_data[0]), len(bus_data[1]))):
            if i < len(bus_data[0]):
                data1 = (bus_data[0][i]).replace(u'→', bus_img)
            else:
                data1 = '&nbsp;'
            if (data1.find(u'科韵路棠安路口站') != -1 and  hour >= 13) or (data1.find(u'综合商业南区站') != -1 and hour < 13):
                self.write('<tr><td bgcolor="#0099CC">')
                self.write(data1)
                self.write('</td>')
            else:
                self.write('<tr><td>')
                self.write(data1)
                self.write('</td>')

            if i < len(bus_data[1]):
                data2 = (bus_data[1][i]).replace(u'→', bus_img)
            else:
                data2 = '&nbsp;'
            if (data2.find(u'科韵路棠安路口站') != -1 and  hour >= 13) or (data2.find(u'综合商业南区站') != -1 and hour < 13):
                self.write('<td bgcolor="#0099CC">')
                self.write(data2)
                self.write('</td></tr>')
            else:
                self.write('<td>')
                self.write(data2)
                self.write('</td></tr>')

        self.write('</table>')
        # self.write('<button style="font-size:40px;color:#FFF;background-color:#888;border:1px solid #E3E9E9;border-radius: 20px;position:fixed;right:15px;bottom:15px;padding-top:60px;padding-bottom:60px;padding-left:100px;padding-right:100px;" onclick="location.reload()">刷新</button>')
        

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/tools/opendoor_mine", MyOpenDoorHandler),
    (r"/tools/opendoor", OpenDoorHandler),
    (r"/bus", CheckBusHandler)
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


