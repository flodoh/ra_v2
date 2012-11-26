'''
Created on 19.11.2012

@author: florian
@funktion: Dies ist der main-controller, der alle wichtigen Funktionen beinhaltet
'''

from model.policy import policy
from commandLineHandler import commandLineHandler

def createPolicy(url,name,text):
        policy1 = policy(url, name, text)
        return policy1
    
def editPolicy(url,name,text):
        policy1 = policy(url, name, text)
        return policy1

if __name__ == '__main__':
    inpuntHandler   =  commandLineHandler()
    inpuntHandler.receiveAndValidateInput()
                
# Objekt der Klasse commandLineHandler wird erstellt. 
# Schleife bis User Programm beendet
    # Dieser ueberprueft Kommmandozeilenparameter formal und gibt Typ der Anfrage und Parameter wie url etc. zurueck
    # Anhand des uebergebenen Typs wie die entsprechende Funktion mit den Paramtern ausgefuehrt