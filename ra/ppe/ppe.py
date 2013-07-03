# -*- coding: utf-8 -*- 
'''
Created on 27.01.2013

@author: florian
@function: this module is the privacy policy extractor. 
For using the module install the pattern library via "pip install pattern"
'''

from pattern.web import Spider, DEPTH, BREADTH, FIFO, LIFO, URL, plaintext
from pattern.db import Datasheet
from pattern.web import Google, URL
from pattern.web import SEARCH
from pattern.vector import Document, Corpus, Bayes
import urllib2
import re, os

Key = ""
KeyActivated = "False"


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
	data = Datasheet.load("../ppe/policy_corpus.csv") #change this path when you call the script directly
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

def findPolicyViaGoogle(query, language, count, pages):
    '''
    gets a query string and other parameters to query the google API.
    returns a list of URL-Objects and the count of requests that were made to
    the google API.
    '''
    global Key
    global KeyActivated
    urls = []
    c = 0
    if KeyActivated is True:
        APIKey = Key
    else:
        APIKey = None

    engine = Google(license=APIKey, language=language, throttle=1.0)
    # Google is very fast but you can only get up to 100 (10x10)
    # results per query.
    for i in range(1, pages + 1):
        c += 1
        for result in engine.search(query, start=i, count=count, type=SEARCH):
            urls.append(URL(result.url))
            #print "Query:", query
            print "URL:", result.url
            #print "Date", result.date
            #print "Author", result.author
            #print "Title:", result.title
            #print "Text html:", result.text
            #print "Text clean:", plaintext(result.text)  # plaintext()
            #removes HTML formatting.
            #print result.download(timeout=10, cached=True, proxy=None) # uses
            #the URL object internally. Same as url.download()
            #print 20 * "-"
    output = [c, urls]
    return output


def extractPolicies(urls, mode, lan, count, pages):
	'''
	This function gets the urls that need to be crawled and the
	mode of finding and extracting the privacy policy on the
	websites
	'''
	if mode == 'crawl':
		# Sort can be switched between LIFO and FIFO
		# LIFO means that the latest link in the queue will be followed first
		# FIFO vice versa
		ppSpiderling = ppSpider (links=urls, domains=["org", "com"], delay=0.1, sort=LIFO)
		while len(ppSpiderling.visited) < 300:
			# DEPTH tells the crawler not to leave the page
			ppSpiderling.crawl(cached=False, method=DEPTH)
	elif mode == 'google':
		for url in urls:
			query = "Datenschutzrichtlinie" + url
			print 10 * "#", "Query:", query, 10 * "#"
			findPolicyViaGoogle(query, lan, count, pages)
	else:
		print "Please choose a valid mode for extracting the policies"

if __name__ == '__main__':
	mode = "google"
	lan = "de"
	pages = 1
	# count of results per page that we collect
	# pages * count = sum of max results per query
	count = 10
	# test set of start urls for running the script 
	# directly in pyton 
	urls = ['http://www.apple.com',
	'http://www.craigslist.com', 
	'http://www.ebay.com', 
	'http://www.facebook.com', 
	'http://www.google.com',
	'http://www.paypal.com', 
	'http://www.tumblr.com', 
	'http://www.twitter.com',  
	'http://www.yahoo.com',
	'http://www.bitly.com']
	extractPolicies(urls, mode, lan, count, pages)