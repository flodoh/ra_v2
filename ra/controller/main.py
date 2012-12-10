'''
Created on 19.11.2012

@author: florian
@function: this controller runs the main loop until the user exits the program
'''
import sys
from util.inputType import *
from executionHandler import *
from model.policy import policy
from commandLineHandler import commandLineHandler

def main():
    
    inputHandler   =  commandLineHandler()
    returnValue = inputHandler.determineOutputDirectory()
    if (1 == returnValue[0]):
         sys.exit(1)
    outputDirectory = returnValue[1]
    firstRun = True
    executioner = executionHandler(outputDirectory)
      
    # during running the program executionStatus is a tuple with 0 (successful) , 1 (error)
    # and error massage dependent on e is printed
    executionStatus = (-1,)
    # TODO: in future check if database connection could be established, if not tell user via commandLine
    while(1):
        #tell the user about success or error of the last execution and get the next VALID task from him
        userInstructions = inputHandler.receiveAndValidateInput(executionStatus,firstRun)
        firstRun = False  
        if(userInstructions == (inputType.exitProgram,"")):
            sys.exit(0)
        else: 
            # execute what the user wants and tell me if it worked or if an error occured
            executionStatus = executioner.execute(userInstructions)    

if __name__ == '__main__':
    main()