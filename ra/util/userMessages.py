'''
Created on 28.11.2012

@author: florian
@function: this is a central collection of all messages that are used more then one time to interact with the user
of the program. If later the code is used for a web app the messages can be easy recylced
'''

class userMessages:
    m0 = "Wrong number of input Parameters, at least one policy needs to be inserted\n\n"
    m1 = "Wrong number of input Parameters, at least one metric needs to be inserted\n\n"
    m2 = "This is no valid command, you can get the list of commands by typing \"help\"\n"
    m3 = "Wrong number of input Parameters, at least one Policy needs to be inserted\n\n"
    exit = "Good Bye"
    urlNotValid = "Sorry, URL is not valid"
    executionSuccessful ="Execution was successful"
    policyNotFound = "Policy not found"
    enterInputDirectory = "Please enter a directory to store the outputData"
    directoryCreationError  = "Could not create directory, pls enter another one"
    policiesAnalyzedSuccessfully ="\nThe Following Policies were analyzed successfully:"
    policiesNotAnalyzedSuccessfully = "\nThe Following Policies were not analyzed successfully:"
    policiesDeletedSuccessfully ="\nThe Following Policies were deleted successfully:"
    policiesNotDeletedSuccessfully = "\nThe Following Policies were not deleted successfully:"