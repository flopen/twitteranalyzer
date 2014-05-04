from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import json
import io



REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "77rid4bwDgdiI5ZRpgej6gTmh"
CONSUMER_SECRET = "wuouNMMCgJMJI3m6xKJyPGJkN1ql7atxrnT4wBqcmkw2hpZx9r"

OAUTH_TOKEN = "2359559589-9WRbVYgYH8TpacYHGwwHxqdXPD3AWKtv01kGMU4"
OAUTH_TOKEN_SECRET = "XM384g07cdxvphrdja9O2xPBJow8S86DdZlCWqQtO0fzF"

URL_QUERY="https://api.twitter.com/1.1/search/tweets.json?q=GabrielGarciaMarquez&count=100&lang=es"
URL_TIMELINE="https://api.twitter.com/1.1/statuses/mentions_timeline.json"

class TwitterReader:
	def get_oauth(self):
	    oauth = OAuth1(CONSUMER_KEY,
	                client_secret=CONSUMER_SECRET,
	                resource_owner_key=OAUTH_TOKEN,
	                resource_owner_secret=OAUTH_TOKEN_SECRET)
	    return oauth

	def get_tweets(self):
		oauth = self.get_oauth()
		r = requests.get(url=URL_QUERY, auth=oauth)
		file_to_save =io.open('tweets.txt', 'w',  buffering=1)
		for tw in r.json()['statuses']:
			file_to_save.write(unicode(u'{0}\n'.format(json.dumps(tw.get('text').replace('\n'," ").replace('\"',' ').replace('\r',' '), ensure_ascii=False))))
		file_to_save.close()

