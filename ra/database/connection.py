'''
Created on 19.11.2012

@author: florian
@funktion: Diese Klasse dient dazu, mit der SQLite-Datenbank "database/db2.db" zu connecten. 
Bei der Persistierung eines Objekts in der Datenbank wird immer das hier angelegte "conn"-Objekt verwendet.
Hierfuer muss die Library "SQLObject" installiert sein (Terminal: sudo easy_install -U SQLObject) und in den
Eclipse-Libraries entsprechend hinzugefuegt werden. 
'''

import sqlobject
from sqlobject.sqlite import builder
conn = builder()('../database/db2.db')

