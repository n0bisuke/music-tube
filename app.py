#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from controllers.tube import *
from controllers.tube_get_oricon import *
from controllers.tweet import *
from controllers.auth import *

#404 Not Found Error
class Error(webapp2.RequestHandler):
    def get(self):
    	self.error(404)
    	path = os.path.join(os.path.dirname(__file__), 'error/404.html')
        return self.response.out.write(template.render(path,""))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/form', MainPage),
    ('/sign', Guestbook),
    ('/get', GetOrikon),
    ('/show', ShowOrikon),
    ('/login', Auth),
    #('/oauth', Oauth),
    ('/n0bisuke_dev_bot_tweet', BotTweetHandler),
    ('/.*', Error),
], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()