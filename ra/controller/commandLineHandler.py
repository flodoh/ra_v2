'''
Created on 21.11.2012
@author: florian
'''
from util.inputType import *
from util.validation import *
from util.userMessages import *
import sys
import os

class commandLineHandler():
    '''
    This class communicates with the user. It welcomes the user and asks him for what to do.
    If the user types something, this class will check if it usable for an action. If not
    the user gets an info that the command is not usable. If a command is valid/ usable
    it will be processed and returned.
    '''
    
    optionList = "Interactions with database\n\
        To insert Policy, please enter:                              insert \"PolicyName\" \"Url of Policy\" \"Company of PolicyFile\" \"Original text of Policy\" \"Updated Text of Policy (optional)\"  \n\
        To delete one or more Policies, please enter:                delete \"Policy A, Policy B, ...\"\n\
        To update a Policy, please enter:                            update \"PolicyName\" \"Field to update (name/url/company/text/updatedText)\" \"New Content\"\n\
        To view all inserted policies, please enter:                 viewPolicies\n\
        To view details of a policy, please enter:                   viewDetails \"PolicyName\" \n\
        \nAnalyze policies\n\
        To apply metrics on one or more policis, please enter:       analyze \"policy A, policy B, ...\"\n\
        To compare all metrics in DB, please enter:                  compareAll\n\
        To compare specific metrics in DB, please enter:             compare \"policy A, policy B, ...\"\n\
        \nPrivacy Policy Extractor (PPE)\n\
        To scrape policies, please enter:                            scrape URL A (http://www.example.com) URL B ... (no \'\"\', no \',\')\n\
        \nAdmin\n\
        To get this option list, please enter:                       help \n\
        " 
    exitMassage = "\nTo exit the program, pls enter:                                      exit  \n"
    welcomeText = "Please choose one option from the list below and enter the appropriate instructions\n(replace expressions between quotes \" \" by adequate names)\n\n"+optionList+exitMassage
   
    def userCommunicator(self, executionStatus, firstRun):
        '''
        Inputs is information about the status of the last communication with the executionHandler()
        and information, if this function is run for the very first time. 
        Task of this method: Communicate with the user, ask him for a command, check this command and if valid
        return it to.
        '''
  
        self.printStatusOfExecution(executionStatus)
        
        return self.receiveAndValidateInput(firstRun)

    
    def printStatusOfExecution(self, executionStatus):
         # if the last execution was successful
        if(executionStatus[0] == 0):
            # if the user want to view all policies
            if(executionStatus[2] == inputType.viewPolicies):
                if len(executionStatus[1]) == 0:
                    print "no policies saved in database"
                for policyName in executionStatus[1]:
                    print policyName
                    
            # if the user wants to view all details of a policy
            elif(executionStatus[2] == inputType.viewDetails):
                policyToView = executionStatus[1]
                print "PolicyName:", '"'+policyToView.name+'",', "Url of Policy:", '"'+policyToView.url+'",', "Company of Policy:", '"'+policyToView.company+'"'
                print "Text of Policy:"
                print '"'+policyToView.text+'"'
                print ""
                print "Updated Text of Policy:"
                print '"'+policyToView.updatedText+'"'
            else:
                print userMessages.executionSuccessful
        # if there was an error last execution
        elif(executionStatus[0] == 1):
            print "Error:", executionStatus[1]
        # if there was success and errors
        elif(executionStatus[0] == 2):
            # if the user wanted to run a1
            if(executionStatus[2] == inputType.analyzePolicies):
                print(userMessages.policiesAnalyzedSuccessfully)
                for policy in executionStatus[1][0]:
                    print(policy)
                print(userMessages.policiesNotAnalyzedSuccessfully)
                for policyTouple in executionStatus[1][1]:
                    print policyTouple[0], "Error:", policyTouple[1] 
             # if the user wanted to run a2
            if(executionStatus[2] == inputType.comparePolicies):
                print(userMessages.policiesAnalyzedSuccessfully)
                for policy in executionStatus[1][0]:
                    print(policy)
                print(userMessages.policiesNotAnalyzedSuccessfully)
                for policyTouple in executionStatus[1][1]:
                    print policyTouple[0], "Error:", policyTouple[1]    
            if(executionStatus[2] == inputType.deletePolicies):
                print(userMessages.policiesDeletedSuccessfully)
                for policy in executionStatus[1][0]:
                    print(policy)
                print(userMessages.policiesNotDeletedSuccessfully)
                for policyTouple in executionStatus[1][1]:
                    print policyTouple[0], "Error:", policyTouple[1]          
  
  
    def receiveAndValidateInput(self, firstRun):
        type = inputType()
       
        while (1):
            #welcome text only after executing first time
            if (firstRun == True):
                print self.welcomeText
                firstRun = False
                
            #collect the command of the user
            input = raw_input()
            
            if input == 'exit':
                print userMessages.exit
                return(type.exitProgram, "")
            inputStrings = list()
            inputStrings = input.split()
            num = len(inputStrings)
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
                            
                elif inputStrings[0] == "update":
                    if(num != 4):
                        print "Wrong number of input Parameters, please check, if you typed all needed parameters. \n\n"
                    else:
                        if (inputStrings[2] =="name" or inputStrings[2] =="url" or inputStrings[2] =="company" or inputStrings[2] =="text" or inputStrings[2] =="updatedText"):
                                validator = validation()
                                if((inputStrings[2] =="url" and validator.isUrlValid(inputStrings[3])) or inputStrings[2] !="url" ):
                                    return (type.updatePolicy,inputStrings[1:])
                                else:
                                    print(userMessages.urlNotValid)
                        else:
                            print "Please choose name, url, company, text or updatedText as a parameter. \n\n"       
                
                elif ((inputStrings[0] == "viewPolicies") & (num == 1)):
                    return (type.viewPolicies,"")
                        
                elif (inputStrings[0] == "viewDetails"):
                    if (num!=2):
                        print "Please give exactly one policy name as a parameter. \n\n"
                    else:
                        return (type.viewDetails, inputStrings[1:])
                                      
                elif inputStrings[0] == "analyze":
                    if(num > 1):
                        return (type.analyzePolicies, inputStrings[1:])
                    else:
                        print userMessages.m0
                
                elif inputStrings[0] == "compare":
                    if(num > 1):
                        return (type.comparePolicies, inputStrings[1:])
                    else:
                        print userMessages.m0
                        
                elif inputStrings[0] == "compareAll":
                    if(num == 1):
                        return (type.compareAllPolicies, inputStrings[1:])
                    else:
                        print userMessages.m1

                # TODO: actually very simple implemented for presentation purpose
                # Later errors need to be caught, URL validation ..
                elif inputStrings[0] == "scrape":
                    if(num > 1):
                        return (type.startPPE, inputStrings[1:])
                    else:
                        print userMessages.m3
                        
                elif inputStrings[0] == "help":
                    print self.optionList
                else:
                    # if the user types bullshit
                    print userMessages.m1
            except IndexError:
                # if the user types nothing
                print userMessages.m1 
  
    
       

        