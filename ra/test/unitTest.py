'''
Created on 19.11.2012

@author: florian
@funktion: Diese Klasse ermoeglicht ein Unit-Testing einzelner Funktionen. 
@comment: Als Interpreter sollte der python unit-test-Interpreter eingesetzt werden. 
Jeder Test muss mit "test_" beginnen, damit der Interpreter ihn erkennt. 
Spaeter macht die Auslagerung bestimmter Tests in eine eigene Testklasse sicher Sinn.
'''
import unittest
from controller.validation import validation
from model.policy import policy

class Test(unittest.TestCase):


    #Test Databaseconnection
    #def test_connectDatabase(self):
    #    policy1 = policy(url='http://test5.de', name='Policy1', text='Dies ist eine Policy')
    #    self.assertTrue(policy1<>False)
        
    #Tests zur Emailvalidierung
    def test_checkEmailValidation(self):
        email1 = "florian@hallo-web.de"
        email2 = "flo@dohmann-web.de"
        email3 = "123@web.de"
        email4 = "web.de"
        email5 = "123"
        email6 = "aa@web.de"
        email7= "hallo@hallo"
        validator = validation()
        isEmailValid = validator.isEmailValid(email1)     
        self.assertTrue(isEmailValid==True)
        isEmailValid = validator.isEmailValid(email2)     
        self.assertTrue(isEmailValid==True)
        isEmailValid = validator.isEmailValid(email3)     
        self.assertTrue(isEmailValid==True)
        isEmailValid = validator.isEmailValid(email4)     
        self.assertTrue(isEmailValid==False)
        isEmailValid = validator.isEmailValid(email5)     
        self.assertTrue(isEmailValid==False)
        isEmailValid = validator.isEmailValid(email6)     
        self.assertTrue(isEmailValid==True)
        isEmailValid = validator.isEmailValid(email7)     
        self.assertTrue(isEmailValid==False)
        
    #Tests zur URL-Validierung
    def test_checkUrlValidation(self):
        url1 = "http://www.hallo.de"
        url2 = "https://www.sicher.nr"
        url3 = "www.test123.de"
        url4 = "test6.com"
        url5 = "123"
        url6 = "http://www.12"
        validator = validation()
        isUrlValid = validator.isUrlValid(url1)     
        self.assertTrue(isUrlValid==True)
        isUrlValid = validator.isUrlValid(url2)     
        self.assertTrue(isUrlValid==True)
        isUrlValid = validator.isUrlValid(url3)     
        self.assertTrue(isUrlValid==True)
        isUrlValid = validator.isUrlValid(url4)     
        self.assertTrue(isUrlValid==True)
        isUrlValid = validator.isUrlValid(url5)     
        self.assertTrue(isUrlValid==False)
        isUrlValid = validator.isUrlValid(url6)     
        self.assertTrue(isUrlValid==False)
        
    
    
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.connectDatabase']
    unittest.main()