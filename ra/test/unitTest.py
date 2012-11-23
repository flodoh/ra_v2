'''
Created on 19.11.2012

@author: florian
@funktion: Diese Klasse ermoeglicht ein Unit-Testing einzelner Funktionen. Als Interpreter sollte der python unit-test-Interpreter eingesetzt werden. 
Jeder Test muss mit "test_" beginnen, damit der Interpreter ihn erkennt
'''
import unittest
from model.policy import policy

class Test(unittest.TestCase):

    #Dieser Test sollte fehlschlagen
    def test_unitTest(self):
        self.assertTrue(True==True)

    #Legt die Tabelle in der Datenbank an, falls noch nicht vorhanden und fuegt einen Datensatz hinzu
    #Muss noch so geschrieben werden, dass Daten angelegt werden, getestet wird, ob es geklappt hat und hinterher wieder geloescht werden.
    #Hier sollten alle Faelee durchgegangen werden, um zu testen, ob Policies wie gewuenscht in der DB gespeichert werden.
    def test_connectDatabase(self):
        policy1 = policy(url='http://test5.de', name='Policy1', text='Dies ist eine Policy')
        self.assertTrue(policy1<>False)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.connectDatabase']
    unittest.main()