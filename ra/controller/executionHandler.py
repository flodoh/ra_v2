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
    by the commandLindeHandler to run the wanted function. It returns: 1. The status (0 for success, 1 for error,
    2 for a mix of success and errors), 2. Additional info like the error, list of policies etc. (Based on the status),
    3. The type of execution. The input for this class needs to be formally valid.
    '''
    def __init__(self,outputDirectory):
        self.outputDirectory = outputDirectory
        
    #Gets the type and all parameters needed to execute the different functions   
    def execute(self, inputData):
        
        # If the user wants to insert a policy
        if(inputData[0] == inputType.insertPolicy):
            return self.createPolicy(inputData[1][0], inputData[1][1], inputData[1][2], datetime.datetime.now(), inputData[1][3], inputData[1][4]) 
        
        # If the user wants to run A1 on single policies    
        elif(inputData[0] == inputType.analyzePolicies):
            return self.runA1(inputData[1], self.outputDirectory)
       
        #If the user wants to viewAllPolices
        elif(inputData[0] == inputType.viewPolicies):
            return self.viewAllPolicies()
        
        #If the user wants to show all details of a policy
        elif(inputData[0] == inputType.viewDetails):
            return self.viewDetails(inputData[1][0])
        
        # If the user wants to update a policy
        elif(inputData[0] == inputType.updatePolicy):
            return self.updatePolicy(inputData[1][0],inputData[1][1],inputData[1][2])
        
        # If the user wants to delete a policy
        elif(inputData[0] == inputType.deletePolicies):
            policyListToDelete = inputData[1]
            return self.deletePolicies(policyListToDelete)
    
    # inserts policy into database, if policyName does not exist in the database yet
    def createPolicy(self, name, url, company, date, text, updatedText):
        try:
            in_file = open(text, "r")
            textContent = in_file.read()
        except Exception as e:
                return(1, e, inputType.insertPolicy)
        try:
            policy(name=name, url=url, company=company, date=date, text=textContent, updatedText=updatedText)
            # except DuplicateEntryError as e:
            #    return (1,e)
        except Exception as e:
            return(1, e, inputType.insertPolicy)
        else: 
            return (0, 0,inputType.insertPolicy)
            
    # analyzes one ore more policies but does not compare them
    def runA1(self, policyList, outputDirectory):
        try:
            ra = ReadabilityAnalyzer()
        except Exception as e:
            return (1,e,inputType.analyzePolicies)
        analyzedPolicies = []
        notAnalyzedPolicies = []
        for policyName in policyList:
            try:
                policyData = policy.select(policy.q.name == policyName)[0]
            except:
                notAnalyzedPolicies.append((policyName,userMessages.policyNotFound))
                continue
            try:
                ra.generate_report(policyData.text, policyName, policyData.url, outputDirectory)
                analyzedPolicies.append(policyName)
            except Exception as e:
                notAnalyzedPolicies.append((policyName,e))
        return(2,(analyzedPolicies,notAnalyzedPolicies),inputType.analyzePolicies)
    
    def viewAllPolicies(self):
        listOfPolicies = []
        try:
            policies = policy.select()
        except Exception as e:
            return(1,e,inputType.viewPolicies)
        
        for policyItem in policies:
            listOfPolicies.append(policyItem.name)
        return  (0, listOfPolicies, inputType.viewPolicies)
    
    def updatePolicy(self, policyName, fieldToUpdate, newContent):
        try:
            policyForUpdate = policy.select(policy.q.name == policyName)[0]
        except IndexError:
            # if policy does not exist, return the message for that
            return (1,userMessages.policyNotFound, inputType.updatePolicy)
        else: 
            # Check, if the given path for the text-file does exist
            if (fieldToUpdate == "text"):
                try:
                    in_file = open(newContent, "r")
                    textContent = in_file.read()
                    policyForUpdate.text = textContent 
                except Exception as e:
                    # if there are problems while opening the file return the error
                    return(1, e, inputType.insertPolicy)
                else:
                    policyForUpdate.text = newContent
            elif (fieldToUpdate == "name"):
                policyForUpdate.name = newContent 
            elif (fieldToUpdate == "url"):
                policyForUpdate.url = newContent
            elif (fieldToUpdate == "company"):
                policyForUpdate.company = newContent
            elif (fieldToUpdate == "updatedText"):
                policyForUpdate.updatedText = newContent
            return  (0, 0, inputType.updatePolicy)
    
    def viewDetails(self, policyName):
            try:
                policyToView = policy.select(policy.q.name == policyName)[0]
            except IndexError:
                # if policy does not exist, return the message for that
                return (1,userMessages.policyNotFound,inputType.viewDetails)
            else:
                return (0,policyToView,inputType.viewDetails)
        
        
    def deletePolicies(self, policyList):
        deletedPolicies = []
        notDeletedPolicies = []
        for policyName in policyList:
            try:
                policyToDelete = policy.select(policy.q.name == policyName)[0]
                policyToDelete.destroySelf()
            except IndexError:
                notDeletedPolicies.append((policyName,userMessages.policyNotFound))
                # if policy does not exist, return the message for that
            else:
                deletedPolicies.append(policyName)
        return (2,(deletedPolicies,notDeletedPolicies),inputType.deletePolicies)

        
        
        