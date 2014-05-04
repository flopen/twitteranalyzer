#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from StopwordHandler import StopwordHandler
from collections import Counter
import re
import json
import io
import unicodedata
class TweetAnalyzer:
	def __init__(self, tweet, id):
		self.stopwords_handler= StopwordHandler()
		self.tweet= tweet
		self.id= id
		self.contador_palabras= self.clean_tweet(tweet)
		self.frecuencia_max=0

		for frec_palabras in self.contador_palabras:
			self.frecuencia_max+=self.contador_palabras[frec_palabras]
		#print self.frecuencia_max
		#self.print_words()

	def clean_tweet(self, tweet):
		result=tweet
		for url in re.findall(r'(https?://[^\s]+)', result):
			result= result.replace(url,"")
		#result = Counter(re.findall(r'\b[^\s\d_]+\b|#\b[^\s\d_]+\b|@\b[^\s\d_]+\b',result.lower(),re.UNICODE))
		result = Counter(re.findall(r'\w+|#\w+|@\w+',result.lower(),re.UNICODE))
		result = self.stopwords_handler.extract_stopwords(result)
		return result

	def print_words(self):
		string_palabras=''
		for p in self.contador_palabras:
			print "++"+p +"++" , self.contador_palabras[p]
			#print p+self.contador_palabras[p]
	def get_counter(self):
		return self.contador_palabras

	def get_max_frec(self):
		return self.frecuencia_max

	def get_id(self):
		return self.id