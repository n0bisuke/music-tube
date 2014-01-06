#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
from models.tubemodel import *

class GetOrikon(webapp2.RequestHandler):
    def get(self):
        import xml.etree.cElementTree as etree
        from google.appengine.api import urlfetch
        
        url = 'http://www.oricon.co.jp/api/ranking/xml/rankingdata.xml'
        xml = urlfetch.fetch(url).content
        dom = etree.fromstring(xml)

        #API情報取得
        date = dom.findall('./status')[0].findtext('date')
        version = dom.findall('./status')[0].findtext('version')
        #self.response.write(date + version)

        #デイリーランキングを取得
        day = dom.findall('./rankingdata/ranking')[0]
        day_format = day.findtext('format')
        day_category = day.findtext('category')
        #self.response.write(day_format + day_category)

        for st in day.findall('./data/item'):
            minfo = {} #連想配列初期化
            minfo["rank"] = st.findtext('rank')
            minfo["title"] = st.findtext('./packageInfo/title')
            minfo["artist"] = st.findtext('./packageInfo/artistName')
            minfo["release"] = st.findtext('./packageInfo/release')
            image_tmp = st.findtext('./packageInfo/img')
            music_image = "<img src='"+ image_tmp +"' />"

            SaveOricon(minfo) #オリコン情報をDBに格納

            self.response.write("%s: %s\n" % (minfo['rank'], minfo['title']))
            self.response.write(music_image)
            self.response.write("%s: %s\n" % (minfo['artist'], minfo['release']) + "<br />")