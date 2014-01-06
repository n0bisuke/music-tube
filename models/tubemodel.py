#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Greeting(db.Model):
    author = db.StringProperty(multiline=True)
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Music(db.Model):
    format = db.StringProperty(multiline=True)
    category = db.StringProperty(multiline=True)
    period = db.StringProperty(multiline=True)
    checkDate = db.StringProperty(multiline=True)
    title = db.StringProperty(multiline=True)
    artistName = db.StringProperty(multiline=True)
    release = db.StringProperty(multiline=True)
    rank = db.StringProperty(multiline=True)
    youtube_id = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

def GreetingFunc():
	return "iii"

def PostGreeting(self):
	greeting = Greeting()
	greeting.author = self.request.get('user')
	greeting.content = self.request.get('content')
	greeting.put()

#曲情報をYOUTUBE検索
#def CheckMusic(minfo):

#曲情報をDBに格納
def SaveMusic(minfo,rank_info):
    MusicModel = Music()
    MusicModel.format = rank_info['format']
    MusicModel.category = rank_info['category']
    MusicModel.period = rank_info['period']
    MusicModel.checkDate = rank_info['checkDate']
    MusicModel.title = minfo['title'] #曲名
    MusicModel.artistName = minfo['artist'] #アーティスト名
    MusicModel.release = minfo['release'] #リリース日
    MusicModel.rank = minfo['rank'] #ランキング
    MusicModel.youtube_id = minfo['youtube_id'] #youtubeのid
    MusicModel.put()