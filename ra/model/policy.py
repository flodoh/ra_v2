'''
Created on 19.11.2012

@author: florian
'''

#import sqlobject
import sqlobject 
from database.connection import conn

# Im Team definieren, was wir fuer Daten zu jeder Policy speichern wollen!! Attribute festlegen!
class policy(sqlobject.SQLObject):
    _connection = conn
    name = sqlobject.StringCol(unique=True);
    url = sqlobject.StringCol();
    company = sqlobject.StringCol();
    date = sqlobject.DateTimeCol()
    text = sqlobject.StringCol()
    updatedText = sqlobject.StringCol()

# create table for policy  
policy.createTable(ifNotExists=True)
