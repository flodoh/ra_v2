'''
Created on 19.11.2012

@author: florian
'''

#import sqlobject
from nltk.tokenize import *
import sqlobject 
from database.connection import conn

# Im Team definieren, was wir fuer Daten zu jeder Policy speichern wollen!! Attribute festlegen!
class policy(sqlobject.SQLObject):
    _connection = conn
    url = sqlobject.StringCol(length=14, unique=True)
    name = sqlobject.StringCol(length=255)
    date = sqlobject.DateTimeCol(default=None)
    text = sqlobject.StringCol()
    
policy.createTable(ifNotExists=True)
