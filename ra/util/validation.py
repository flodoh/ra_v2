'''
Created on 26.11.2012

@author: florian
@function: Validierung von Strings hinsichtlich definierter erwarteter Werte wie z.B. Emailadressen
'''
import re

class validation():

    def isEmailValid(self,email):
        if len(email) < 7:
            return False
        elif re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                return True
        else:
            return False
        
    #regEx eventuell noch nicht optimal    
    def isUrlValid(self,url):
        if re.match("^(https?://)?(([\w!~*'().&=+$%-]+: )?[\w!~*'().&=+$%-]+@)?(([0-9]{1,3}\.){3}[0-9]{1,3}|([\w!~*'()-]+\.)*([\w^-][\w-]{0,61})?[\w]\.[a-z]{2,6})(:[0-9]{1,4})?((/*)|(/+[\w!~*'().;?:@&=+$,%#-]+)+/*)$",url) != None:
            return True
        else:
            return False


#class MyClass(object):
#    '''
#    classdocs
#    '''

#    def __init__(selfparams):
#        '''
#        Constructor
#        '''
        