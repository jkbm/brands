from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
from db import addtwits

ckey = "1dO3pJN85Bv0GEUOhmlWV0jPi"
csecret = "Yi8uI1A8eBfOXrSfMyeXetguFpBZX6l3eAvtGHeILnS5SkpHxb"
atoken = "43292116-dKxSuEzNLFIW7ACZvseHjjnNWoa7YtnkkRiy22aOd"
asecret = "koAHbIv8ewVVIgeMmH60d3elXzPLmFjzyXx4Yv9vKxAg5"

#seek = raw_input("What to search? ")
#file = raw_input("File name: ")
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

