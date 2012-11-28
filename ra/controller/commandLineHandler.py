'''
Created on 21.11.2012

@author: florian
@function: Anzeige der moeglichen Optionen fuer den User, Entgegennahme und Ueberpruefung der
Formalen Anforderungen an die Eingabe (wie z.B. Emailformat, numerische Werte..)
Rueckgabewert ist eine eindeutige Nummer, die der Weiterverarbeitung dient
'''
from inputType import *

class commandLineHandler():
    
    optionList = "Interactions with database\n\
        To delete one or more Policies, please enter:              delete \"policy A, policy B, ...\"\n\
        To insert Policy, please enter:                            insert \"PolicyName\" \"Url of Policy\" \"Name of PolicyFile\"  \n\
        To view all inserted policies, please enter:               viewPolicies\n\
        \nAnalyze policies\n\
        To add metrices to default metrices, please enter:         add \"metric A, metric B, ...\"\n\
        To remove metrices from default metrices, please enter:    subtract \"metric A, metric B, ...\"\n\
        To apply metrices on one or more policies, please enter:   anylalyze \"policy A, policy B, ...\"\n\
        " 
    exitMassage = "\nTo exit the program, pls enter:                                    exit  \n"
    welcomeText = "Please choose one option from the list below and enter the appropriate instructions\n(replace expressions between quotes \" \" by adequate names)\n\n"+optionList+exitMassage
   
    def receiveAndValidateInput(self):
        type = inputType()
        while (1):
            print self.welcomeText
            input = raw_input()
            if input == 'exit':
                return(type.exitProgramm, "")
            inputStrings = input.split();
            num = len(inputStrings)
            if inputStrings[0] == "delete":
                if(num < 2):
                    print "Wrong number of input Parameters, at least one Policy needs to be inserted\n\n"
                else:
                    return (type.deletePolicies, inputStrings[1:])
                
            elif inputStrings[0] == "insert":
                if(num !=4):
                    print "Wrong number of input Parameters, this option takes exactly four parameters\n\n"
                else:
                    #evtl Ueberpruefung, ob url www enthaelt
                    return (type.insertPolicy, inputStrings[1:])
                
            elif ((inputStrings[0] == "viewPolicies") & (num == 1)):
                return (type.viewPolicies,"")
             
            elif inputStrings[0] == "add":
                if(num > 1):
                    return (type.addMetrics, inputStrings[1:])
                else:
                    print("Wrong number of input Parameters, at least one metric needs to be inserted\n\n")
             
            elif inputStrings[0] == "substract":
                if(num > 1):
                    return (type.subtractMetric, inputStrings[1:])
                else:
                    print("Wrong number of input Parameters, at least one metric needs to be inserted\n\n")
                    
            elif inputStrings[0] == "analyze":
                if(num > 1):
                    return (type.analyzePolicies, inputStrings[1:])
                else:
                    print("Wrong number of input Parameters, at least one policy needs to be inserted\n\n")
            else:
                print("Wrong parameters inserted!\n\n") 
                
# class MyClass(object):
#    '''
#    classdocs
#    '''
# 
#    def __init__(self):
#        '''
#        Constructor
#        '''
#
        