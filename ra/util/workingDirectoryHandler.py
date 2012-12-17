'''
Created on 12.12.2012

@author: Simon
'''
import os
from userMessages import *

def determineWorkingDirectory():
        
        currentdir = os.getcwd()
        #checks if a outPutDirectory.txt file exists, which contains the outputdirectory, maybe change the location of this file
        workingDirectoryFile = False
        workingDirectory= ''
        FirstRun = True
        try:
            #dont know if this works at all os
            utilDirectory = currentdir+"\..\util"
            in_file = open(utilDirectory+"/workingDirectory.txt", "r")
            workingDirectory = in_file.read()
            workingdirectoryFile = True
        except IOError as e:
            while(1):
                # ask the user to type in the directory
                print userMessages.workingDirectory
                try:
                    workingDirectory = raw_input()
                    break
                except Exception as e:
                    return(1,e)


        while(1):
            if(FirstRun == True):
                FirstRun = False
            else:
                workingDirectory = raw_input()
            if(fatherDirectoryExists(workingDirectory) == False):
                print "Error: FatherDirectory of working directory:\"", workingDirectory,"\"does not exist, please enter another one"
                continue
            if(workingDirectoryFile == False):
                try:
                    os.mkdir(workingDirectory)
                    break
                except Exception as e:
                    print "Error: directory already exists, please enter another one"
                print "Working Directory\"", workingDirectory, "\" succesfully created "
                workingDirectoryFile = True
            break
        if(workingDirectoryFile  == False):
            outputFile = open(utilDirectory+"/workingDirectory.txt", "w")
            outputFile.write(workingDirectory)
        return (0,workingDirectory)

def fatherDirectoryExists(workingDirectory):
    numberOfSlahs = workingDirectory.count('/')
    if(numberOfSlahs == 0):
        return False
    stringSize = len(workingDirectory)
    if(workingDirectory[stringSize-1] == '/' ):
         workingDirectory = workingDirectory[:-1]
    fatherDirectory = workingDirectory[:workingDirectory.rfind('/')]
    
    return os.path.isdir(fatherDirectory)
    
