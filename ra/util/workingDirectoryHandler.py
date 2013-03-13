'''
Created on 12.12.2012

@author: Simon
'''
from shutil import copytree, ignore_patterns, copy
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
                
            if((workingDirectoryFile == False) or  not((os.path.isdir(workingDirectory)))):
                htmloutput = currentdir+"/../output/html_output/"
                template1 = currentdir+"/../output/template.html"
                template2 = currentdir+"/../output_comparison/template.html"
                try:
                    #all hidden folders (starting with .) are ignored
                    copytree(htmloutput, workingDirectory, ignore = ignore_patterns('.*'))
                #    print htmloutput+"template.html"
                    os.makedirs(workingDirectory+"/output/")
                    os.makedirs(workingDirectory+"/output_comparison/")
                    copy(template1, workingDirectory+"/output/")
                    copy(template2, workingDirectory+"/output_comparison/")            
                 #   copy(template1, workingDirectory)
                  #  copy(template2, workingDirectory)       
                    print "Working Directory\"", workingDirectory, "\" succesfully created "
                    break
                except Exception as e:
                    print "Error: directory already exists, please enter another one"
                    continue
            break
        if((workingDirectoryFile == False) or  workingDirectory != workingDirectoryOld):
            outputFile = open(utilDirectory+"/workingDirectory.txt", "w")
            outputFile.write(workingDirectory)
            outputFile.close()
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
    
