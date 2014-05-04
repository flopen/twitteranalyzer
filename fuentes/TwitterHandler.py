#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from StopwordHandler import StopwordHandler
from collections import Counter
from TweetAnalyzer import TweetAnalyzer
from TwitterReader import TwitterReader
import re, math
import json
import io
import unicodedata
import numpy 
import codecs

FILE_TWEETS="tweets.txt"
RELATION_NAME="GarciaMarquezTweets"
LOGGER_FILE="logger.txt"
FILE_COSINE_SIMILARITY_MATRIX="matriz_similitud_por_coseno.arff"
FILE_TF_IDF_MATRIX="matriz_tf_idf.arff"

class TwitterHandler:
	def __init__(self):
		self.logger= io.open(LOGGER_FILE, encoding='utf-8', mode='w+',  buffering=1)
		self.write_in_logger("Iniciando...")
		self.tweetsword= Counter()
		self.tweets_hash=[]
		reader=TwitterReader()
		reader.get_tweets()
		self.write_in_logger("Buscar Twitters...OK")

	def write_in_logger(self,log):
		self.logger.write(unicode(u'{0}\n'.format(log)))

	def main(self):
		file_tw =io.open(FILE_TWEETS, 'r',  buffering=1)
		lines = file_tw.readlines()
		id=0
		for tw in lines:
			#print tw
			t_aux= TweetAnalyzer(tw,id)
			self.tweets_hash.append(t_aux)
			id+=1
			self.get_unique_words(t_aux.get_counter())

		self.do_vector_model_arff()
		self.write_in_logger("Haciendo matriz TF IDF...OK")
		self.do_cosine_similarity_matrix()
		self.write_in_logger("Haciendo matriz similitud por coseno...OK")

	def get_unique_words(self, tweet_hash):
		for word_in_tweet in tweet_hash:
			self.tweetsword[word_in_tweet]+=1

	def do_cosine_similarity_matrix(self):
		documentos=self.get_cosine_similarity_matrix(self.tweets_hash)
		names=[]
		index=0
		for i in documentos:
			names.append('Twitter-{0}'.format(index))
			index+=1

		self.write_arff_file(file_name=FILE_COSINE_SIMILARITY_MATRIX, names_arff= names, data_arff=documentos)

	def do_vector_model_arff(self):
		N=len(self.tweets_hash)

		self.matrix= numpy.zeros((N,len(self.tweets_hash)))

		idfs=[]
		ftis_d=[]

		for ni in self.tweetsword:
			IDFi= float(numpy.log10(N/self.tweetsword[ni]))
			idfs.append({'Ni': ni, 'IDFi': IDFi})

		for tw_h in self.tweets_hash:
			ftis=[]
			tw_h_counter= tw_h.get_counter()
			#print "actual::", tw_h.get_id()
			mod=0
			for tw_c in tw_h_counter:
				fti=   float(tw_h_counter[tw_c] )#/ tw_h.get_max_frec())
				ftis.append({'ki': tw_c, 'fti': fti})
			ftis_d.append({'Di':tw_h.get_id(), 'ftis': ftis})
	
		documentos=[]

		for doc in ftis_d:
			documentos.append(self.build_matrix(idfs,doc))		

		self.write_arff_file_spacrse(file_name=FILE_TF_IDF_MATRIX, data_arff=documentos)
		#self.show_results(idfs, ftis_d,documentos)

	def get_cosine_similarity_matrix(self, documentos):
		docs=[]
		for i in documentos:
			counter1=i.get_counter()
			di=[]
			#print counter1
			for j in documentos: 
				counter2=j.get_counter()
				cos=self.get_cosine(counter1,counter2)
				#print cos				
				di.append(cos)
			docs.append(di)
		return docs

	def build_matrix(self, idfs, doc):
		di=[]
		di_a=[]
		fxi=0
		words_in_doc= doc.get('ftis')
		modulo= self.get_modulo(words_in_doc)
		for idf in idfs:
			fxi=round(float(0.0000), 3)
			for p_in_doc in words_in_doc: 
				if p_in_doc.get('ki')==idf.get('Ni'):
					fxi= round(float(p_in_doc.get('fti') /modulo * idf.get('IDFi')), 3) #/ numpy.sqrt(mod))
			di.append(fxi)
		return di

	def get_modulo(self, datos):
		modulo=0
		for d in datos: 
			modulo+= d.get('fti')*d.get('fti')
		return math.sqrt(modulo)
		
	def  show_results(self, idfs, ftis_d, documentos):
		print "\nPalabras totales: " ,len(self.tweetsword)
		for tp in self.tweetsword:
			print tp, ": ",self.tweetsword[tp]
		print "\nIDF:"
		for idf in idfs:
			print idf.get('Ni'),": ",idf.get('IDFi')
		print "\nFTS::"
		for ft in ftis_d:
			print ft.get('Di'), ": ",ft.get('ftis')

		print "\nMatriz columnas: "
		for i in self.tweetsword:
			print i
		print "\nMatriz filas: "
		for d in documentos: 
			print d


	def get_cosine(self,vec1, vec2):
	     intersection = set(vec1.keys()) & set(vec2.keys())
	     numerator = sum([vec1[x] * vec2[x] for x in intersection])

	     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	     denominator = math.sqrt(sum1) * math.sqrt(sum2)

	     if not denominator:
	        return 0.0
	     else:
	        return round(float(numerator) / denominator, 3)
	def get_names_for_arff(self,tweetsword):
		names_arff=[]
		for word in self.tweetsword:
			names_arff.append(word)
		return names_arff

	def write_arff_file_spacrse(self, file_name= "1.arrf" ,realion_arff= RELATION_NAME,data_arff=[]):
		names_arff=self.get_names_for_arff(self.tweetsword)
		fp= io.open(file_name, encoding='utf-8', mode='w+',  buffering=1) 
		fp.write(unicode(u'@RELATION {0}\n'.format(RELATION_NAME)))
	
		
		for name in names_arff: 
			#fp.write(unicode(u'{0}'.format(' ')))
			fp.write(unicode(u'@ATTRIBUTE {0} real\n'.format(name)))
			#fp.write(unicode(u'{0}\n'.format(' real')))
		fp.write(unicode(u'{0}\n'.format('@DATA')))
		
		for data in data_arff:
			fp.write(unicode(u'{0}'.format('{')))
			i=1
			primero=0
			for d in data:
				p= d * i
				if p>0 and primero==0:				
					fp.write(unicode(u'{0} {1}'.format(i-1,p)))
					primero=1
				elif p>0:
					fp.write(unicode(u', {0} {1}'.format(i-1,p)))

				i+=1
			fp.write(unicode(u'{0}\n'.format('}')))	
	
	def write_arff_file(self, file_name= "1.arrf" ,realion_arff= RELATION_NAME, names_arff=[], data_arff=0): 
		fp= io.open(file_name, encoding='utf-8', mode='w+',  buffering=1) 
		fp.write(unicode(u'@RELATION {0}\n'.format(RELATION_NAME)))
		for name in names_arff: 
			#fp.write(unicode(u'{0}'.format(' ')))
			fp.write(unicode(u'@ATTRIBUTE {0} real\n'.format(name)))
			#fp.write(unicode(u'{0}\n'.format(' real')))
		fp.write(unicode(u'{0}\n'.format('@DATA')))
		for data in data_arff:
			primero=0
			for d in data:
				if d>=0 and primero==0:				
					fp.write(unicode(u'{:3.3f}'.format(d)))
					primero=1
				elif d>=0:
					fp.write(unicode(u',{:3.3f}'.format(d)))
			fp.write(unicode(u'\n'))

	

if __name__ == "__main__":
	twh=TwitterHandler()
	twh.main()
   
