#!/usr/bin/env python
# -*- coding: utf-8 -*-

FILE_SPANISH1="stop-words/stop-words_spanish_1_es.txt"
FILE_SPANISH2="stop-words/stop-words_spanish_2_es.txt"

class StopwordHandler:
	def __init__(self):
		self.words = []
		words=self.stopwords()

	def stopwords(self):
		stopwords_file1= open(FILE_SPANISH1)
		stopwords_file2= open(FILE_SPANISH2)
		self.words=[]
		self.do_array(stopwords_file1)
		self.do_array(stopwords_file2)
		#print self.words

	def do_array(self, stopwords_file):
		for line in stopwords_file:
			line= line.strip()
			if(line!=""):
				self.words.append(unicode (line,'utf-8') )
		
	def extract_stopwords(self,text):
		for w in self.words:
			text.pop(w, None)
		return text