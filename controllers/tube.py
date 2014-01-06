#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
import os
from google.appengine.ext.webapp import template
from models.tubemodel import *

class ShowOrikon(webapp2.RequestHandler):
    def get(self):
        import json
        import random

        #gqlをjsonにいい感じに変換
        def gql_json_parser(query_obj):
            result = []
            for entry in query_obj:
                result.append(dict([(p, unicode(getattr(entry, p))) for p in entry.properties()]))

            random.shuffle(result) #シャッフル
            return result

        greetings_query = Music.gql("WHERE youtube_id != 'false'")
        json_query_data = gql_json_parser(greetings_query)

        #ヘッダー情報
        self.response.headers['Content-Type'] = 'application/json'
        #json出力
        self.response.out.write(json.dumps(json_query_data,indent=4))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = ""
        path = os.path.join(os.path.dirname(__file__), '../views/play.html')
        self.response.out.write(template.render(path, template_values))

#フォーム
class MainPage(webapp2.RequestHandler):
    def get(self):

        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        url = "http://google.com"
        url_linktext = 'google'
        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
            }
        path = os.path.join(os.path.dirname(__file__), '../views/index.html')
        self.response.out.write(template.render(path, template_values))

        s = Music.gql("WHERE title = :title", title=u"ナノ・セカンド")
        self.response.write(s[0].rank + ":")
        self.response.write(s[0].title + "<hr>")

class Guestbook(webapp2.RequestHandler):
    def post(self):
        # greeting = Greeting()
        # greeting.author = self.request.get('user')
        # greeting.content = self.request.get('content')
        # greeting.put()
        PostGreeting(self)
        self.redirect('/')