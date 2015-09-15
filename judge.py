import os
import tornado.web
import tornado.ioloop
import problemset.problems
__author__ = 'nekocode'


class JudgeHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('hello world!')
        self.write('<a style="display:none;">' + problemset.problems.key1 + '</a>')


if __name__ == '__main__':
    settings = {
        'static_path': os.path.join(os.path.dirname(__file__), 'static')
    }

    application = tornado.web.Application([
        (r'/', JudgeHandler),
        (r'/' + problemset.problems.key1, problemset.problems.Problem1Handler),
        (r'/' + problemset.problems.key3, problemset.problems.Problem3Handler),
        (r'/' + problemset.problems.key4, problemset.problems.Problem4Handler),
        (r'/' + problemset.problems.key5, problemset.problems.Problem5Handler),
        (r'/' + problemset.problems.key6, problemset.problems.Problem6Handler)
    ], **settings)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

