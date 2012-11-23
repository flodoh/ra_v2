'''
Created on 19.11.2012

@author: florian
@funktion: Dies ist der main-controller, der alle wichtigen Funktionen beinhaltet
'''

from model.policy import policy
import sys

def createPolicy(url,name,text):
        policy1 = policy(url, name, text)
        return policy1
    
def editPolicy(url,name,text):
        policy1 = policy(url, name, text)
        return policy1

# erstes Testkonstrukt zum prinzipiellen Aufbau der Konsolenbefehle    
def main():
    finish=False
    while finish==False:
            try:
                input = raw_input("Please choose from the list")
                if input == 'exit':
                    break
                x = int(input)     
                print x
            except ValueError as e:
                print "Oops!  That was no valid number.  Try again...", e

if __name__ == '__main__':
        main()  
                
# Objekt der Klasse commandLineHandler wird erstellt. 
# Schleife bis User Programm beendet
    # Dieser ueberprueft Kommmandozeilenparameter formal und gibt Typ der Anfrage und Parameter wie url etc. zurueck
    # Anhand des uebergebenen Typs wie die entsprechende Funktion mit den Paramtern ausgefuehrt