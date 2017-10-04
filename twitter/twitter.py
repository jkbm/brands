#!/usr/bin/python2.7
# -*- encoding: utf-8 -*-
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
from db import addtwits

auth = open("mysite/twitter/auth.json", "r")
auth_json = json.load(auth)

ckey = auth_json['CONSUMER_KEY']
csecret = auth_json['CONSUMER_SECRET']
atoken = auth_json['OAUTH_TOKEN']
asecret = auth_json['OAUTH_TOKEN_SECRET']

num = 0
tweets = ""
def stream(file,seek, n, res):
	seek = u""+seek+""
	class listener(StreamListener):
		def on_data(self,data):
			try:
				if num <= n:
					global num
					num += 1
					saveNum = open('num.txt', 'w')
					saveNum.write(str(num))
					global tweets
					saveNum.close()
					text = json.loads(data)
					tex = text['text'].decode('latin1').encode('utf-8')
					saveFile = open('/home/jekabm/mysite/files/' + file + '.csv', 'a')
					tweets = tweets + "||" + tex
					saveFile.write(tex)
					saveFile.write("\n")
					saveFile.close()
					addtwits(text['id'], int(res), text['user']['id'], tex, text['user']['screen_name'])
					return True
				else:
					return False
			except BaseException, e:
				print "Failed: " + str(e)
				time.sleep(5)

	def on_error(status):
		print status

	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=[seek],languages=['en'], filter_level='low')
	return tweets

