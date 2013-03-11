# -*- coding: utf-8 -*- 
'''
Created on 27.01.2013

@author: florian
@function: this module is the privacy policy extractor. 
For using the module install the pattern library via "pip install pattern"
'''

from pattern.web import Spider, DEPTH, BREADTH, FIFO, LIFO
from pattern.db import Datasheet
from pattern.vector import Document, Corpus, Bayes
from nltk.tokenize import RegexpTokenizer
from nltk.classify import NaiveBayesClassifier as nbc
import re, os

class NaiveBayesClassifier():

    def __init__(self, training_data1, training_data2):
        self._training_set = self._create_taining_set(training_data1, training_data2)
        self._classifier = nbc.train(self._training_set)

    def _create_taining_set(self, training_data1, training_data2):
    	training_set = []
       	training_text = open(training_data1).read()
        words = tokenize(training_text)
        training_set += [(dict([(word, True)]), "policy") for word in words]

        training_text = open(training_data2).read()
        words = tokenize(training_text)
        training_set += [(dict([(word, True)]), "no_policy") for word in words]

    	return training_set

    def classify(self, text):
        result = {}
        prob_dist = self._classifier.prob_classify(self._create_dict(text))
        for label in self._classifier.labels():
            result[label] = prob_dist.prob(label)
        return result

    def _create_dict(self, text):
        words = tokenize(text)
        return dict([(word, True) for word in words])

def classifyPolicy(content):
	'''
	gets a pre-qualified html content
	and returns if it contains a policy or not 
	'''
	data = Datasheet.load("policy.corpus.csv")
	documents = []
	for score, message in data:
		document = Document(message, type=int(score) > 0)
		documents.append(document)
	corpus = Corpus(documents)
	print "number of documents", len(corpus)

def checkIfPolicy(url):
	'''
	gets the crawled url
	returns True if the url is a potential
	candidate for uncluding a policy and False if not
	'''
	flags = (re.UNICODE | re.MULTILINE | re.IGNORECASE)
	policyExp = re.compile(ur"policy",flags)
	privacyExp = re.compile(ur"privacy",flags)
	if policyExp.search(url) or privacyExp.search(url):
		return True
	else:
		return False


class ppSpider(Spider):
    
    def visit(self, link, source=None):
        print "visiting:", link.url, "from:", link.referrer
        # Do the pre filtering via Regular Expression
        if checkIfPolicy(link.url) == True:
        	print "Found a policy in", link.url
        	print source
        	#classifyPolicy(source)
        else:
  			print "No Policy found"


    def fail(self, link):
        print "failed:", link.url


def extractPolicies(urls):
	ppSpiderling = ppSpider (links=urls, domains=["org"], delay=0.0)
	while len(ppSpiderling.visited) < 300:
		ppSpiderling.crawl(cached=False)
	# 'Microsoft', 
	# 'Amazon', 
	# 'Twitter', 
	# 'LinkedIn', 
	# 'Wordpress', 
	# 'Ebay', 
	# 'Apple', 
	# 'Paypal', 
	# 'Tumblr', 
	# 'BBC', 
	# 'Livejasmin', 
	# 'Craigslist', 
	# 'Ask'

def tokenize(text, regex=u'[a-zA-ZäöüÄÖÜß0-9]+', tolower=True):

    tokenizer = RegexpTokenizer(regex, flags=re.UNICODE)
    if tolower:
        text = text.lower()
    tokens = tokenizer.tokenize(text)
    return tokens


if __name__ == '__main__':
	# test set of policies
	urls = ['http://www.google.com',
	'http://www.facebook.com', 
	'http://www.youtube.com', 
	'http://www.yahoo.com', 
	'http://en.wikipedia.org', 
	'http://www.amazon.com']
	extractPolicies(urls)
