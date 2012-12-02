'''
Created on 28.11.2012

@author: Simon
@function: Diese Klasse bekommt die vom commandLineHandler verifizierte
Eingabe und fuehrt die entsprechende Funktion aus. Der Rueckgabewert ist entweder 
0 fuer eine erfolgreiche Execution oder ein Tupel aus 1 und dem zugehoerigen Error
'''
from model.policy import *
import datetime
from util.inputType import *
from util.userMessages import *
from sqlobject.dberrors import *
from readability.readabilityanalyzer import *
class executionHandler():
    '''
    This class is responsible for executing all major functions in this program. It gets the commands
    by the commandLindeHandler to run the wanted function. It returns an info about success or error of execution.
    '''
   
    #TODO: Shell we put this function together with the others to a "policy_controler"?
    def __createPolicy (self, name, url, company, date, text, updatedText):
        newPolicy=policy(name=name, url=url, company=company, date=date, text=text, updatedText=updatedText)
        return newPolicy
        
    #Gets the type and all parameters needed to execute the different functions
    def execute(self, input):
        
        # If the user wants to insert a policy
        if(input[0] == inputType.insertPolicy):
            try:
                in_file = open(input[1][3], "r")
                textContent = in_file.read()
            except Exception as e:
                 return(1, e, inputType.insertPolicy)
            try:
                self.__createPolicy(input[1][0], url=input[1][1], company = input[1][2],
                         date = datetime.datetime.now(), text = textContent,
                         updatedText = input[1][4])
            # except DuplicateEntryError as e:
            #    return (1,e)
            except Exception as e:
                return(1, e, inputType.insertPolicy)
            else: 
                return (0, 0,inputType.insertPolicy)
            
        # If the user wants to run A1 on single policies    
        elif(input[0] == inputType.analyzePolicies):
            try:
                ra = ReadabilityAnalyzer()
            except Exception as e:
                return (1,e,inputType.analyzePolicies)
            analyzedPolicies = []
            notAnalyzedPolicies = []
            for policyName in input [1]:
                try:
                    policyData = policy.select(policy.q.name == policyName)[0]
                except:
                    notAnalyzedPolicies.append((policyName,userMessages.policyNotFound))
                    continue
                try:
                    ra.generate_report(policyData.text, policyName, policyData.url)
                    analyzedPolicies.append(policyName)
                except Exception as e:
                    notAnalyzedPolicies.append((policyName,e))
            return(2,(analyzedPolicies,notAnalyzedPolicies),inputType.analyzePolicies)