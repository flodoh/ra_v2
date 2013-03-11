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
from ppe.ppe import *

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
       
       # If the user wants to run A2 on some Policies    
        elif(inputData[0] == inputType.comparePolicies):
            return self.runA2(inputData[1], self.outputDirectory)

       # If the user wants to run A2 on some Policies    
        elif(inputData[0] == inputType.compareAllPolicies):
            return self.runA2(inputData[1], self.outputDirectory)     
       
        #If the user wants to viewAllPolices
        elif(inputData[0] == inputType.viewPolicies):
            return self.viewAllPolicies()
        
        #If the user wants to show all details of a policy
        elif(inputData[0] == inputType.viewDetails):
            return self.viewDetails(inputData[1][0])
        
        # If the user wants to update a policy
        elif(inputData[0] == inputType.updatePolicy):
            return self.updatePolicy(inputData[1][0],inputData[1][1],inputData[1][2])

        # If the user wants to start the PPE
        elif(inputData[0] == inputType.startPPE):
            return self.startPPE(inputData[1])
        
        # If the user wants to delete a policy
        elif(inputData[0] == inputType.deletePolicies):
            policyListToDelete = inputData[1]
            return self.deletePolicies(policyListToDelete)
    
    # inserts policy into database, if policyName does not exist in the database yet
    # TODO: read in also the Content of updatedText 
    def createPolicy(self, name, url, company, date, text, updatedText):
        
        try:
            in_fileText = open(text, "r")
            textContent = in_fileText.read()
        except Exception as e:
                return(1, e, inputType.insertPolicy)
        if (updatedText == ""):
            updatedTextContent = ""
        else:
            try:
                in_fileUpdatedText = open(updatedText, "r")
                updatedTextContent = in_fileUpdatedText.read()
            except Exception as e:
                    return(1, e, inputType.insertPolicy)
        try:
            policy(name=name, url=url, company=company, date=date, text=textContent, updatedText=updatedTextContent)
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
    
    def runA2(self, policyList, outputDirectory):
        try:
            ra = ReadabilityAnalyzer()
        except Exception as e:
            return (1,e,inputType.comparePolicies)
        
        policyResult = self.get_policies_by_names(policyList)  
        data = policyResult[0]
        
        foundPolicyNames = []      
        for policy in policyResult[1]:
            foundPolicyNames.append(policy.name)
            
        notFoundPolicyNames = []
        for policy in policyResult[2]:
            notFoundPolicyNames.append(policy.name)
        try:
            ra.create_benchmark(data, outputDirectory)
        except Exception as e:
                notFoundPolicyNames.append((foundPolicyNames))
                print e

        return(2,(foundPolicyNames,notFoundPolicyNames),inputType.comparePolicies)

    def viewAllPolicies(self):
        listOfPolicies = []
        try:
            policies = policy.select()
        except Exception as e:
            return(1,e,inputType.viewPolicies)
        
        for policyItem in policies:
            listOfPolicies.append(policyItem.name)
        return  (0, listOfPolicies, inputType.viewPolicies)
    
    # updates one value of one policy-dataset in the database
    def updatePolicy(self, policyName, fieldToUpdate, newContent):
        try:
            policyForUpdate = policy.select(policy.q.name == policyName)[0]
        except IndexError:
            # if policy does not exist, return the message for that
            return (1,userMessages.policyNotFound, inputType.updatePolicy)
        else: 
            # Read in the Content of the file with the given path
            if (fieldToUpdate == "text"):
                try:
                    in_file = open(newContent, "r")
                    textContent = in_file.read()
                    policyForUpdate.text = textContent 
                except Exception as e:
                    # if there are problems while opening the file return the error
                    return(1, e, inputType.updatePolicy)
            elif (fieldToUpdate == "updatedText"):
                try:
                    in_file = open(newContent, "r")
                    textContent = in_file.read()
                    policyForUpdate.updatedText = textContent 
                except Exception as e:
                    # if there are problems while opening the file return the error
                    return(1, e, inputType.updatePolicy)
            elif (fieldToUpdate == "name"):
                policyForUpdate.name = newContent 
            elif (fieldToUpdate == "url"):
                policyForUpdate.url = newContent
            elif (fieldToUpdate == "company"):
                policyForUpdate.company = newContent
            return  (0, 0, inputType.updatePolicy)
    
    # returns the policy-dataset (if existent) from the database, so that its details can be displayed in later programm execution
    def viewDetails(self, policyName):
            try:
                policyToView = policy.select(policy.q.name == policyName)[0]
            except IndexError:
                # if policy does not exist, return the message for that
                return (1,userMessages.policyNotFound,inputType.viewDetails)
            else:
                return (0,policyToView,inputType.viewDetails)
        
     
    # deletes one or more policiy-datasets from the database (if existend) and returns the list of deleted (existent) and not deleted (not existent)  policy-datasets 
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

    def startPPE (self, urls):
        extractPolicies(urls)
        return (0,0, inputType.startPPE)
        
    def get_policies_by_names(self, policyNames):
        
        policyList = []
        foundPolicies = []
        notFoundPolicies = []
        if(len(policyNames) == 0):
            try:
                foundPolicies = policy.select()
            except Exception as e:
                    return(1,e,inputType.viewPolicies)
        else:
            for policyName in policyNames:
                try:
                    policyData = policy.select(policy.q.name == policyName)[0]
                    foundPolicies.append(policyData)
                except Exception as e:
                    notFoundPolicies.append(policyName)
                    continue

        data = {}
        
        for policyItem in foundPolicies:
                    
            name = policyItem.name
            data[name] = {}
            data[name]["name"] = policyItem.name
            data[name]["text"] = policyItem.text
            data[name]["url"] = policyItem.url
            data[name]["date"] =  policyItem.date
        
        return (data, foundPolicies, notFoundPolicies)
       
        