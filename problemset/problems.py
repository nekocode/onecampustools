import tornado.web
import hashutils
__author__ = 'nekocode'


key1 = hashutils.md5('welcome')
key2 = hashutils.md5('post')
key3 = hashutils.md5('base64')      # 95a1446a7120e4af5c0c8878abb7e6d2
key4 = hashutils.md5('js')          # 32981a13284db7a021131df49e6cd203
key5 = hashutils.md5('hahahaha')    # 4f0b36a34946153c358f8b243428a1eb
key6 = hashutils.md5('good job!')    # a729936b9d88fada272fe80979cea09a


class Problem1Handler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('problem1')
        self.write('<a style="display:none;">md5(post) and then post to this page</a>')

    def post(self, *args, **kwargs):
        if self.request.body == key2:
            self.write(key3)


class Problem3Handler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('UEsDBBQAAAAIANl6LkdUsccXBAAAAAIAAAAKAAAAcmVhZG1lLnR4dMsqBgBQSwECPwAUAAAACADZei5HVLHHFwQAAAACAAA'
                   'ACgAkAAAAAAAAACAAAAAAAAAAcmVhZG1lLnR4dAoAIAAAAAAAAQAYAPUtgyi+7tABucNSEL7u0AG5w1IQvu7QAVBLBQYAAA'
                   'AAAQABAFwAAAAsAAAAAAA=')


class Problem4Handler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.render("js.html")


class Problem5Handler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        argument = self.get_argument('pwd', None)
        if argument == '72019':
            self.write('key: ' + key6)
        elif argument:
            self.write('wrong')
        else:
            self.write('pwd = [0~99999]')


class Problem6Handler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('Congratulation!')

