#!/usr/bin/env python
# -*- coding:utf-8 -*-
import webapp2
import os
from extends.GAE_Oauth import oauth

class Auth(webapp2.RequestHandler):
    def get(self):
        sessionID = binascii.hexlify(os.urandom(8))
        self.response.out.write(sessionID)

#さきほど取得した各情報をここで指定する
TWITTER_CONSUMER_KEY = 'BpG9VBdL2UepklE8KHVJPQ'
TWITTER_CONSUMER_SECRET = 'WBUO6GiO8mHvyAd1ATSKzgzSfzs1sCPtv5Ie4bFU'
TWITTER_ACCESS_TOKEN = '2229531270-lZ4deSCbyvquXFWPAgA1WocQnuRTOV9qvGaOQJm'
TWITTER_ACCESS_TOKEN_SECRET = 'HvZ3Zov2V4WP0fjfol1YoCbMAgkBoBQW5bj8Fx6taKmwM'

class BotTweetHandler(webapp2.RequestHandler):
  def get(self):
    client = oauth.TwitterClient(TWITTER_CONSUMER_KEY,
                                 TWITTER_CONSUMER_SECRET, None)
    tweet = u"おはようさん"
    param = {'status': tweet}
    client.make_request('https://api.twitter.com/1.1/statuses/update.json',
                        token=TWITTER_ACCESS_TOKEN,
                        secret=TWITTER_ACCESS_TOKEN_SECRET,
                        additional_params=param,
                        protected=True,
                        method='POST')
    self.response.out.write(tweet)