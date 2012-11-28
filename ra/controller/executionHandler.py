'''
Created on 28.11.2012

@author: Simon
@function: Diese Klasse bekommt die vom commandLineHandler verifizierte
Eingabe und fuehrt die entsprechende Funktion aus. Der Rueckgabewert ist entweder 
ein Error oder True, wenn die Aktion erfolgreich war
'''
import sqlite3

from model.policy import *
import datetime
from inputType import *
from sqlobject.dberrors import *
class executionHandler():
    
    #Gets the type and all parameters needed to execute the different functions
    def execute(self, input):
        if(input[0] == inputType.insertPolicy):
            
            try:
                policy(name = input[1][0], url=input[1][1], company = input[1][2],
                         date = datetime.datetime.now(), text = input[1][3],
                         updatedText = input[1][4])
            # except DuplicateEntryError as e:
            #    return (1,e)
            except Exception as e:
                return(1, e)
            else: 
                return (0,)
            
                  
# class MyClass(object):
#    '''
#    classdocs
#    '''

#    def __init__(selfparams):
#        '''
#        Constructor
#        '''