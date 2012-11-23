#Generate specific html file (report) for each Policy
#Simply reads template file and generates specific html page into html_output
import sys
import os
#Template Path (hardcoded)
TEMPLATE = "report_template.html"

def get_template():
    f = open(TEMPLATE, 'r')
    templ = f.read()
    f.close()
    return templ

def save_report(content, pol_name):
    currentdir = os.curdir
    #print currentdir
    filename = currentdir + "/html_output/" + pol_name + ".html"
    f = open(filename, "w")
    f.writelines(content)
    f.close()

def substitute(params):
    templ = get_template()
    
    return

save_report("42", "testpl")
    
    


