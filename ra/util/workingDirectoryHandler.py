'''
Created on 12.12.2012

@author: Simon
'''
import distutils.dir_util
import os
from userMessages import *


def determineWorkingDirectory():
        
        currentdir = os.getcwd()
        #checks if a outPutDirectory.txt file exists, which contains the outputdirectory, maybe change the location of this file
        workingDirectoryFile = False
        workingDirectory= ''
        workingDirectoryOld = ''
        FirstRun = True
        try:
            #dont know if this works at all os
            utilDirectory = currentdir+"/../util"
            in_file = open(utilDirectory+"/workingDirectory.txt", "r")
            workingDirectoryOld = in_file.read()
            in_file.close()
            workingDirectory = workingDirectoryOld
            workingDirectoryFile = True
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
                print "Error: FatherDirectory of working directory:\"", workingDirectory,"\" does not exist, please enter another one"
                continue
            if(os.path.isdir(workingDirectory)):
               a = 2
            if((workingDirectoryFile == False) or  not((os.path.isdir(workingDirectory)))):
                htmloutput = currentdir+"/../output/html_output/"
                try:
                    os.mkdir(workingDirectory)                
                    distutils.dir_util.copy_tree(htmloutput, workingDirectory)
                    distutils.dir_util.copy_tree(htmloutput, workingDirectory)
                    distutils.dir_util.copy_tree(htmloutput, workingDirectory)
                    print "Working Directory\"", workingDirectory, "\" succesfully created "
                    break
                except Exception as e:
                    print "Error: directory already exists, please enter another one"
                    continue
            break
               # workingDirectoryFile = True
            #break

        if(workingDirectoryFile  == False):
            outputFile = open(utilDirectory+"/workingDirectory.txt", "w")
            outputFile.write(workingDirectory)
            outputFile.close()
        #workingDirectory#.decode('base64')
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
    
