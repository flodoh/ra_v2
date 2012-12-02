'''
Created on 21.11.2012
@author: florian
'''
from util.inputType import *
from util.validation import *
from util.userMessages import *
import sys

class commandLineHandler():
    '''
    This class communicates with the user. It welcomes the user and asks him for what to do.
    If the user types something, this class will check if it usable for an action. If not
    the user gets an info that the command is not usable. If a command is valid/ usable
    it will be processed and returned.
    '''
    
    optionList = "Interactions with database\n\
        To insert Policy, please enter:                              insert \"PolicyName\" \"Url of Policy\" \"Company of PolicyFile\" \"Original Text of Policy\" \"Updated Text of Policy (optional)\"  \n\
        To delete one or more Policies, please enter:                delete \"policy A, policy B, ...\"\n\
        To view all inserted policies, please enter:                 viewPolicies\n\
        \nAnalyze policies\n\
        To add metrics to default metrics, please enter:             add \"metric A, metric B, ...\"\n\
        To remove metrics from default metrics, please enter:        subtract \"metric A, metric B, ...\"\n\
        To apply metrics on one or more policis, please enter:       analyze \"policy A, policy B, ...\"\n\
        \nAdmin\n\
        To get this option list, please enter:                       help\n\
        " 
    exitMassage = "\nTo exit the program, pls enter:                                      exit  \n"
    welcomeText = "Please choose one option from the list below and enter the appropriate instructions\n(replace expressions between quotes \" \" by adequate names)\n\n"+optionList+exitMassage
   
    def receiveAndValidateInput(self, executionStatus, firstRun):
        '''
        Inputs is information about the status of the last communication with the executionHandler()
        and information, if this function is run for the very first time. 
        Task of this method: Communicate with the user, ask him for a command, check this command and if valid
        return it to.
        '''
        type = inputType()
        if(executionStatus[0] == 0):
            print userMessages.executionSuccessful
        elif(executionStatus[0] == 1):
            print "Error:", executionStatus[1]
        elif(executionStatus[0] == 2):
            if(executionStatus[2] == inputType.analyzePolicies):
                print('\nThe Following Policies were analyzed succesfully')
                for policy in executionStatus[1][0]:
                    print(policy)
                print('\nThe Following Policies were not analyzed succesfully')
                for policyTouple in executionStatus[1][1]:
                    print policyTouple[0], "Error:", policyTouple[1] 
        while (1):
            #welcome text only after executing first time
            if (firstRun == True):
                print self.welcomeText
                firstRun = False
            input = raw_input()
            if input == 'exit':
                print userMessages.exit
                return(type.exitProgram, "")
            #TODO: funktioniert derzeit nur mit einem Wort als text
            inputStrings = list()
            inputStrings = input.split()
            num = len(inputStrings)
            #try faengt den error, wenn der user nichts eingibt
            try:
                if inputStrings[0] == "delete":
                    if(num < 2):
                        print "Wrong number of input Parameters, at least one Policy needs to be inserted\n\n"
                    else:
                        return (type.deletePolicies, inputStrings[1:])
                    
                elif inputStrings[0] == "insert":
                    if((num != 5) and (num != 6) ):
                        print "Wrong number of input Parameters, this option takes either four or five parameters\n\n"
                    else:
                        validator = validation()
                        if(validator.isUrlValid(inputStrings[2])):
                            # Wenn kein optionaler "updated Text" eingegeben wurde
                            if(num == 5):
                                inputStrings.append("")
                            return (type.insertPolicy, inputStrings[1:])
                        else:
                            print userMessages.urlNotValid
                    
                elif ((inputStrings[0] == "viewPolicies") & (num == 1)):
                    return (type.viewPolicies,"")
                 
                elif inputStrings[0] == "add":
                    if(num > 1):
                        return (type.addMetrics, inputStrings[1:])
                    else:
                        print userMessages.m1
                 
                elif inputStrings[0] == "substract":
                    if(num > 1):
                        return (type.subtractMetric, inputStrings[1:])
                    else:
                        print userMessages.m1
                        
                elif inputStrings[0] == "analyze":
                    if(num > 1):
                        return (type.analyzePolicies, inputStrings[1:])
                    else:
                        print userMessages.m0
        
                elif inputStrings[0] == "help":
                    print self.optionList
                else:
                    print userMessages.m2 
            except IndexError:
                print userMessages.m2 
                
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
        