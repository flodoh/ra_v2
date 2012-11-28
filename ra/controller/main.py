'''
Created on 19.11.2012

@author: florian
@funktion: Dies ist der main-controller, der alle wichtigen Funktionen beinhaltet
'''
import sys
from inputType import *
from executionHandler import *
from model.policy import policy
from commandLineHandler import commandLineHandler

def createPolicy(url,name,text):
        policy1 = policy(url, name, text)
        return policy1
    
def editPolicy(url,name,text):
        policy1 = policy(url, name, text)
        return policy1

def main():
    inputHandler   =  commandLineHandler()
    executioner = executionHandler()
    # during running the program executionStatus is a tuple with 0 (successful) , 1 (error)
    # and error massage dependent on e is printed
    executionStatus = (-1,)
    # in future check if database connection could be established, if not tell user via commandLine
    while(1):
        userInstructions = inputHandler.receiveAndValidateInput(executionStatus)
        if(userInstructions == (inputType.exitProgram,"")):
            sys.exit(0)
        else: 
            # fuehre eine Aktion aus
            executionStatus = executioner.execute(userInstructions)       
    #the execution of the instructions will be implemented here


if __name__ == '__main__':
   main()
                
# Objekt der Klasse commandLineHandler wird erstellt. 
# Schleife bis User Programm beendet
    # Dieser ueberprueft Kommmandozeilenparameter formal und gibt Typ der Anfrage und Parameter wie url etc. zurueck
    # Anhand des uebergebenen Typs wie die entsprechende Funktion mit den Paramtern ausgefuehrt