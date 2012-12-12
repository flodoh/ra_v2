'''
Created on 19.11.2012

@author: florian
@function: this controller runs the main loop until the user exits the program
'''
import sys
from util.inputType import *
from util.userMessages import *
from util.workingDirectoryHandler import determineWorkingDirectory
from executionHandler import *
from model.policy import policy
from commandLineHandler import commandLineHandler


def main():
    
    print userMessages.programmStarted,"\n"
    inputHandler   =  commandLineHandler()
    returnValue = determineWorkingDirectory()
    if (1 == returnValue[0]):
         sys.exit(1)
    outputDirectory = returnValue[1]
    firstRun = True
    executioner = executionHandler(outputDirectory)
      
    # during running the program executionStatus will exist of 3 informations: 1. The status (0 for success, 1 for error,
    # 2 for a mix of success and errors), 2. Additional info like the error, list of policies etc. (Based on the status),
    # 3. The type of execution
    executionStatus = (-1,)
    # TODO: in future check if database connection could be established, if not tell user via commandLine
    while(1):
        #tell the user about success or error of the last execution and get the next VALID task from him
        userInstructions = inputHandler.userCommunicator(executionStatus,firstRun)
        firstRun = False  
        if(userInstructions == (inputType.exitProgram,"")):
            sys.exit(0)
        else: 
            # execute what the user wants and tell me if it worked or if an error occured
            executionStatus = executioner.execute(userInstructions)    

if __name__ == '__main__':
    main()