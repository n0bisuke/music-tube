#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
import xml.etree.cElementTree as etree
import json
import urllib2
from google.appengine.api import urlfetch
from models.tubemodel import *

#Youtube DATA APIで動画検索してIDを返す
def Youtube(artist,title):
    s = artist+"%20"+title
    #s = "ゴールデンボンバー%20１０１回目の呪い"
    #s = "舞祭組%20棚からぼたもち"
    #s = "Ｒｉｄｅ　Ｗｉｔｈ　Ｍｅ%20Ｈｅｙ！Ｓａｙ！ＪＵＭＰ"
    search = s.replace("　", "%20") #空白が入って来た場合に%20に置換
    #search = "ゆず%20表裏一体"
    url = 'http://gdata.youtube.com/feeds/api/videos?'
    url += 'vq="'+search #検索内容
    url += '"&orderby=relevance' #関連性が高い動画
    url += '&start-index=1' #1位から検索開始
    url += '&max-results=1' #上位1つ ?
    url += '&alt=json' #フォーマットをJSONに
    #JSONから再生URLを取得
    data = urlfetch.fetch(url)
    j = json.loads(data.content)
    #検索ヒット件数
    result = j['feed']['openSearch$totalResults']['$t']
    if result == 0:
        return 'false'
    
    youtube_url = j['feed']['entry'][0]['link'][-1]['href']
    #再生URLからIDを取得
    tmp = youtube_url.split('/')
    youtube_id = tmp[-1]
    return str(youtube_id)

class GetOrikon(webapp2.RequestHandler):
    def get(self):
        url = 'http://www.oricon.co.jp/api/ranking/xml/rankingdata.xml'
        xml = urlfetch.fetch(url).content
        dom = etree.fromstring(xml)

        #hoge = Youtube("ゴールデンボンバー","１０１回目の呪い")
        #hoge = Youtube("Ｈｅｙ！Ｓａｙ！ＪＵＭＰ","Ｒｉｄｅ　Ｗｉｔｈ　Ｍｅ")
        #hoge = Youtube("浜崎あゆみ","Ｆｅｅｌ　ｔｈｅ　ｌｏｖｅ／Ｍｅｒｒｙ−ｇｏ−ｒｏｕｎｄ")
        #hoge = Youtube("ももいろクローバーＺ","「泣いちゃいそう冬／鋼の意志」ももクリ　２０１３＜ＬＩＶＥ会場＆キングＥ−ＳＨＯＰ＞期間限定シングル【２０１３年１２月２３日ＬＩＶＥ＠西武ドーム】")
        #self.response.write(hoge)
        #API情報取得
        # date = dom.findall('./status')[0].findtext('date')
        # version = dom.findall('./status')[0].findtext('version')

        #<ranking>を抜き出す
        ranking = dom.findall('./rankingdata/ranking')
        for item in ranking:
            rank_info = {} #ランキング情報配列初期化
            rank_info['format'] = item.findtext('format')
            if rank_info['format'] == 'dvd': #formatがdvdのモノは削除
                break
            rank_info['category'] = item.findtext('category')
            rank_info['period'] = item.findtext('period')
            rank_info['checkDate'] = item.findtext('data/date')

            for st in item.findall('./data/item'):
                minfo = {} #曲情報配列初期化
                minfo["rank"] = st.findtext('rank')
                minfo["title"] = st.findtext('./packageInfo/title')
                minfo["artist"] = st.findtext('./packageInfo/artistName')
                minfo["release"] = st.findtext('./packageInfo/release')
                image_tmp = st.findtext('./packageInfo/img')
                music_image = "<img src='"+ image_tmp +"' />"
                #Youtube検索してIDを取得
                minfo["youtube_id"] = Youtube(minfo["artist"].encode('utf_8'),minfo["title"].encode('utf_8'))                
                SaveMusic(minfo,rank_info) #曲情報をDBに格納
                
                # self.response.write("%s: %s\n" % (rank_info['category'], rank_info['checkDate']))
                # self.response.write("%s: %s\n" % (minfo['rank'], minfo['release']))
                # self.response.write(music_image)
                self.response.write("%s:%s" % (minfo['artist'], minfo['title']))
                self.response.write("<hr />")