#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
from tornado.options import define,options,parse_command_line
import sys
import logging

define("port", default=8080, help="port to listen on",type=int)
tornado.options.parse_command_line()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world!")

def make_app():
    return tornado.web.Application([ (r"/", MainHandler), ])  # URL Mapping

if __name__ == "__main__":
    
    app = make_app()
#   application = tornado.web.Application(handlers, debug=options.debug)
    try:
        if(options.port==8080):
           app.listen(options.port)
           logging.info("Server Listening on default port: http://localhost:%s/" % options.port)
        else:
           app.listen(options.port)
           logging.info("Server Listening on http://localhost:%s/" % options.port)

        tornado.ioloop.IOLoop.current().start()
    except Exception as e:
        print("Error: "+str(e))
