#coding=latin-1
'''
Created on 05.12.2011

@author: Marcus Voss
'''
import matplotlib
import matplotlib.pyplot as line_plt
from pylab import *


class LineChart(object):

    def create(self, data):
       
        #Array mit Werten erstellen
        site_values = []
        scores = data.keys()
        score_labels = []
        
        for score in scores:
            if score <> "Flesch Reading Ease" and score <> "LIX" and score <> "RIX" and score <> "New Dale Chall":
                site_values.append(data[score])
                score_labels.append(score)
        
        y = []
        i = 0
        while i < len(score_labels):
            y.append(i)
            i = i + 1
            
        fig = line_plt.figure()

        yticks(arange(len(score_labels)), score_labels)
  
        plot(site_values, y, "o-")
        
        ylim([0 - 0.5, len(score_labels) - 0.5])
        xlim([0, max(site_values) + 0.1])

    def draw(self, data):
        self.create(data)
        show()
        
    def save(self, data, path='line_chart.png'):
        self.create(data)
        savefig(path, format = 'png')

if __name__ == "__main__":
    data = {}
    scores = ["Flesch", "RIX", "Dale-Chall", "SMOG"]
    
    for score in scores:
        data[score] = rand()
      
    lc = LineChart()
    lc.draw(data)