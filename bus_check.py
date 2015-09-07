#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib2
import json
# import re
import time
from bs4 import BeautifulSoup
__author__ = 'nekocode'


def deal_page(page):
    soup = BeautifulSoup(page, from_encoding="utf8")
    lis = soup.find_all('li')
    _bus_data = []
    for li in lis:
        # print li.find('div', {'class': re.compile('num *')}).text
        flag = 0
        busies = li.find_all('div', {'class': 'bus'})
        for bus in busies:
            if not bus.has_attr('style'):
                flag = 1
            else:
                flag = 2

        station_name = li.find('div', {'class': 'station'}).text
        if flag == 0:
            _bus_data.append(u'　　　' + station_name)
        elif flag == 1:
            _bus_data.append(u'－》　' + station_name)
        elif flag == 2:
            _bus_data.append(u'　　　' + station_name)
            _bus_data.append(u'－》　')

    return _bus_data


def get_bus_data():
    hour = time.strftime('%H', time.localtime())
    urls = ['http://m.tool.finded.net/index.php?m=Bus&c=Bus&a=refresh&l=kcRiyrpC-1x3qA-3xJcEGuSolw-2x-2x%2F',
            'http://m.tool.finded.net/index.php?m=Bus&c=Bus&a=refresh&l=hK1PjB4ragFWS30H-3xqJZCw-2x-2x%2F']
    bus_data = []

    for url in urls:
        if hour < 13:
            url += '1'  # 上午
        else:
            url += '0'
        header = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3) AppleWebKit/533.1 (KHTML, like Gecko) '
                                'Version/4.0 Mobile Safari/533.1'}
        http = httplib2.Http(timeout=10)
        response, content = http.request(url, 'GET', headers=header)
        content = content[3:]  # 去除BOM
        data = json.loads(content)
        if data['status'] == 1:
            stations = deal_page(data['info'])
            # if hour < 13:
            #     stations.
            bus_data.append(stations)
        else:
            bus_data.append([])

    return bus_data
