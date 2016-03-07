# encoding = utf-8
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        myfile = self.request.files['myfile']
        for content in myfile:
            print content
        # fin = open(myfile['filename'], "wb+")
        # fin.write(myfile['body'])
        # fin.close()


application = tornado.web.Application([(r'/upload', UploadHandler),
                                      (r'/', MainHandler)])

if __name__ == '__main__':
    application.listen(8011)
    tornado.ioloop.IOLoop.instance().start()