#!/usr/bin/python
'''
Created on 19.12.2011

@author: Marcus Voss
'''
import matplotlib
from pylab import *

class box_plot(object):
    '''
    classdocs
    '''
    def draw(self, data = {}):
       
        #Array mit Werten erstellen
        values = []
        site_values = []
        
        sites = data.keys()
        scores = data[data.keys()[0]].keys()
        
        for site in sites:
            for score in scores:
                site_values.append(data[site][score])
            values.append(site_values)
            site_values = []

        a = array(values)
  
        boxplot(a)

        #fig.canvas.set_window_title('A Boxplot Example')

        xticks(arange(len(scores))+1, scores)
        show()

if __name__ == "__main__":
    data = {}
    sites = ["Facebook", "Google", "Microsoft", "IBM", "StudiVZ"]
    scores = ["Flesch", "RIX", "Dale-Chall", "SMOG"]
    
    for site in sites:
        data[site] = {}
        for score in scores:
            data[site][score] = rand()
      
    bp = box_plot()
    bp.draw(data)