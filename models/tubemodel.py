#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Greeting(db.Model):
    author = db.StringProperty(multiline=True)
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Oricon(db.Model):
    title = db.StringProperty(multiline=True)
    artistName = db.StringProperty(multiline=True)
    release = db.StringProperty(multiline=True)
    rank = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

def GreetingFunc():
	return "iii"

def PostGreeting(self):
	greeting = Greeting()
	greeting.author = self.request.get('user')
	greeting.content = self.request.get('content')
	greeting.put()

#オリコン情報をDBに格納
def SaveOricon(minfo):
    OriconModel = Oricon()
    OriconModel.title = minfo['title']
    OriconModel.artistName = minfo['artist']
    OriconModel.release = minfo['release']
    OriconModel.rank = minfo['rank']
    OriconModel.put()