# -*- coding: utf-8 -*- 
'''
Created on 10.04.2013

@author: florian
@function: This script is used for measuring the ratio of string 
equality. It was used to check whether the PPEs cleaning process
meets the demand.
'''

from difflib import SequenceMatcher

# One example for the comparison of alle extracted texts from apple

# load the manually extracted policy
file1 = open("corpora/yahoo.txt").read()

# load the automatically full extracted html

file2 = open("similarity_matching/yahoo1.html").read()

# load the html after deletion of boilerplates
file3 = open("similarity_matching/yahoo2.html").read()

# load the raw policy automatically extracted out of the loaded html
file4 = open("similarity_matching/yahoo3.txt").read()


print "Comparing Original and full html. Ratio:"
s = SequenceMatcher(lambda x: x == " \t\n", file1, file2)
print round (s.ratio(), 3)

print "Comparing Original and html without boilerplates. Ratio:"
s = SequenceMatcher(lambda x: x == " \t\n", file1, file3)
print round (s.ratio(), 3)

print "Comparing Original and extracted raw policy. Ratio:"
s = SequenceMatcher(lambda x: x == " \t\n", file1, file4)
print round (s.ratio(), 3)

