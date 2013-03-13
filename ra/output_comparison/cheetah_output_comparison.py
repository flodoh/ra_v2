# Smarter way of implementation (to prevent redundant code): 
# one cheetah_output file with the possibilities to generate normal report and comparison report 
# (only diff is the template.html, dict and output dir) 

import os
import string
import random
from Cheetah.Template import Template

#TEMPLATE = '../output_comparison/template.html'
#TEMPLATE = '../output_comparison/template.html'

#needs an dict with all the params
def substitute(values, fry, heatmap, template):
    table_begin = """
    <table class="condensed-table">
    <thread>
        <th>SITE</th> 

        <th>Flesch Reading Ease</th>
        <th>Flesch-Kincaid</th>    
        <th>RIX</th> 
        <th>Coleman-Liau</th> 
        <th>Gunning Fog</th> 
        <th>New Dale Chall Score enhanced</th> 
        <th>New Dale Chall Grade</th> 
        <th>New Dale Chall grade enhanced</th> 
        <th>New Dale Chall</th> 
        <th>ARI</th>         
        <th>SMOG</th>  
        <th>LIX</th>  
 
        </thread>
        <tbody  class="zebra-striped">
        """
    table_content =""
    
    # ADDED: for each of the policies and the corresponding measures 
    for site in values:
        cell = "" 
        col_content = """<tr>
        <td>""" + str(site) + """ </td> """
                    
        for v in values[site]['scores'].iteritems(): 
            val = v[1]
            cell_add = """
                        <td>""" + str(round(val, 2)) + """</td>
                    """
            cell = cell + cell_add       

        col_content = col_content + cell + """</tr>"""
        table_content = table_content + col_content
        
    table_end = """        
        </tbody>    
            </table>"""
    table = table_begin + table_content + table_end
    
    template_values = {}
    template_values['table'] = str(table)
    template_values['heatmap'] = heatmap
    template_values['fry_graph'] = fry
    
    #ADDED: write all html-content in one string (from template
    t = Template(file=template, searchList=template_values)
    
    return str(t)

def save_report(content, name, outputDirectory):
    #save t as pol_name.html in /outputDirectory/
    filename = outputDirectory+ "/output_comparison/" + name + ".html"
    f = open(filename, "w")
    f.write(content)
    f.close()
    open_report(filename)

def open_report(path):
    path = os.path.abspath(path)
    
    #command oeffnet am Ende direkt die html im Browser. Methode ist nur mit Windows kompatibel.
    #os.startfile(path)

def name_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
    
def create_report(dict, fry, heatmap, outputDirectory, single_rep = False):
    template = outputDirectory+'/output_comparison/template.html'
    new_report = substitute(dict, fry, heatmap, template)
    filename = name_gen()
    save_report(new_report, filename, outputDirectory)
