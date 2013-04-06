# -*- coding: utf-8 -*- 
'''
Created on 27.01.2013

@author: florian
@function: this module is the privacy policy extractor. 
For using the module install the pattern library via "pip install pattern"
'''

from pattern.web import Spider, DEPTH, BREADTH, FIFO, LIFO, URL, plaintext
from pattern.db import Datasheet
from pattern.vector import Document, Corpus, Bayes
import urllib2
import re, os


def classifyPolicy(content):
	'''
	gets a pre-qualified html content
	and returns if it contains a policy or not.
	TODO: This function needs to be finished
	The trainingset needs to be modified
	'''
	# The corpus does not have an empty line 
	# between the end of a policy and the new 
	# policy
	data = Datasheet.load("policy_corpus.csv")
	documents = []
	for score, message in data:
		document = Document(message, type=int(score) > 0)
		documents.append(document)
	corpus = Corpus(documents)
	print "number of documents:", len(corpus)
	print "number of words:", len(corpus.vector)
	print "number of words (average):", sum(len(d.terms) for d in corpus.documents) / float(len(corpus))
	print
	classifier = Bayes()
	for document in corpus:
		classifier.train(document)
	print "Is it a policy?", classifier.classify(content)
	return True

def checkIfPolicy(url):
	'''
	gets the crawled url
	returns True if the url is a potential
	candidate for having a policy and False if not
	'''
	flags = (re.UNICODE | re.MULTILINE | re.IGNORECASE)
	policyExp = re.compile(ur"policy",flags)
	privacyExp = re.compile(ur"privacy",flags)
	if policyExp.search(url) or privacyExp.search(url):
		return True
	else:
		return False

def cleanHtml(html):
	'''
	gets the html document as a string and
	and retrurns the cleaned raw text
	'''
	# check pattern documentation for modification (http://www.clips.ua.ac.be/pages/pattern-web#plaintext)
	text = plaintext(html)
	return text

def deleteBoilerplates(url):
	'''
	gets the link to a website,
	sends it to the boilerplate API,
	and returns the cleaned html from
	the http response 
	'''
	# check pattern documentation for modification (http://www.clips.ua.ac.be/pages/pattern-web#plaintext)
	req = urllib2.Request('http://boilerpipe-web.appspot.com/extract?url='+url)
	result = urllib2.urlopen(req)
	return result.read()


class ppSpider(Spider):
    def visit(self, link, source=None):
        print "visiting:", link.url, "from:", link.referrer
        # Do the pre filtering via Regular Expression
        if checkIfPolicy(link.url) == True:
        	print "Found a policy in", link.url
        	print source
        	print 10 * "----"
        	noBoilerplates = deleteBoilerplates(link.url)
        	print noBoilerplates
        	print 10 * "----"
        	if noBoilerplates == "":
        		print "Problems with the Boilerpipe API"
        	else:
        		cleanPage = cleanHtml(noBoilerplates)
        		print cleanPage
        		print 10 * "----"
        		if classifyPolicy(cleanPage) is True:
        			# loadToDatabase() # needs to be implemented
        			print 20 * "-"
        			print "Info: No policy saved to DB because classifier/trainingset needs to be optimized."
        			print 20 * "-"

        else:
  			print "No Policy found"


    def fail(self, link):
        print "failed:", link.url


def extractPolicies(urls):
	ppSpiderling = ppSpider (links=urls, domains=["org", "com"], delay=0.0)
	while len(ppSpiderling.visited) < 300:
		ppSpiderling.crawl(cached=False)


if __name__ == '__main__':
	# test set of start urls for running the script 
	# directly in pyton 
	urls = ['http://www.google.com',
	'http://www.facebook.com', 
	'http://www.youtube.com', 
	'http://www.yahoo.com', 
	'http://en.wikipedia.org', 
	'http://www.amazon.com'
	extractPolicies(urls)
