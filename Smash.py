# -*- coding: utf-8 -*-
import time
import requests
import json
import collections
import random
import tweepy
import credentials
import markovify
import argparse
import subprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import numpy




class Smash :
  
	
        def __init__(self, name):
            self.screen_name = name


	def preProcessOfData(self,post):
		processed_post_text = []
		for word in post["text"].split(" "):
			if (
					len(word) > 0 and       # Remove empty strings
					word[0] != '@' and      # Remove at mentions and usernames
					word[0] != '/' and      # Remove emojis and some weird stuff
					"http" not in word and  # Remove links
					"RT" not in word):      # Remove RTs
				processed_post_text.append(word)
		return " ".join(processed_post_text)


	def makeShortUrl(self,long_url):
		# Use the goo.gl api to shorten a link
		post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + \
				   credentials.api_key
		params = json.dumps({'longUrl': long_url})
		response = requests.post(post_url, params, headers={'Content-Type': 'application/json'})
		return response.json()['id']


	def generateTweetWithMarkov(self,screen_name, timeline, short_url):
		processed_timeline_text = [self.preProcessOfData(post) for post in timeline]
                print processed_timeline_text
		text_model = markovify.Text(processed_timeline_text)
		return "@" + screen_name + " " + text_model.make_sentence() + short_url


	def postTweet(self,text):
		auth = tweepy.OAuthHandler(credentials.consumer_key,credentials.consumer_secret)
		auth.set_access_token(credentials.access_token,credentials.access_token_secret)
		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
		api.update_status(text)
		time.sleep(5);


	def getUserTimeline(self,depth):
		auth = tweepy.OAuthHandler(credentials.consumer_key,credentials.consumer_secret)
		auth.set_access_token(credentials.access_token,credentials.access_token_secret)
		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

		timeline = []
		for page_num in xrange(depth):
			timeline.extend(api.user_timeline(screen_name=self.screen_name,count=100,include_rts=False,page=page_num))
		return timeline

		
	
short_url = "http://xxx.xxxxx" ##Malicious link
if __name__ == '__main__':

    # Read list of potential targets from file
    with open("target.txt", 'r') as targets_file:
        potential_targets = [target.strip() for target in targets_file]

    for screen_name in potential_targets:
            newTarget =  Smash(screen_name)
            timeline = newTarget.getUserTimeline(50)
	    tweet = newTarget.generateTweetWithMarkov(screen_name,timeline,short_url);
	    newTarget.postTweet(tweet)

main()
