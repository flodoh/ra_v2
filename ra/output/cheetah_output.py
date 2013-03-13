import os
from Cheetah.Template import Template

#TEMPLATE = '../output/template.html'


# Substitutes the Template with policy specific values
def substitute(values, template):
    table_begin = """
    <table class="condensed-table">
    <thread>
        <th>Measure</th>
        <th>Exact Number</th>    
        </thread>
        <tbody  class="zebra-striped">
        """
        
    table_content = ""
    
    for s, v in values['scores'].iteritems(): 
        cell = """
                <tr>
                    <td>""" + str(s) + """</td>
                    <td>""" + str(round(v, 2)) + """</td>
                </tr>"""
        table_content = table_content + cell
            
    table_end = """        
        </tbody>    
            </table>"""
            
    table = table_begin + table_content + table_end
    values['table'] = str(table)
    
    t = Template(file=template, searchList=values)
    
    return str(t)

def save_report(content, name, outputDirectory):
    #save t as pol_name.html in /html_ouput/
    #currentdir = os.curdir
    #filename = "../output/html_output/" + name + ".html"
    filename = outputDirectory + "/" + name + ".html"
    print filename
    f = open(filename, "w")
    f.write(content)
    f.close()
    open_report(filename)

def open_report(path):
    path = os.path.abspath(path)
    
    #oeffnet direkt den Browser. Funktioniert aber nur bei Windows
    #os.startfile(path)
    
def create_report(dict,outputDirectory):
    print "outputDirectory", outputDirectory
    template = outputDirectory+'/output/template.html'
    new_report = substitute(dict, template)
    save_report(new_report, dict["name"], outputDirectory)