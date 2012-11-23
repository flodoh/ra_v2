#!/usr/bin/python
# coding=utf-8
'''
Created on 19.12.2011

@author: Marcus Voss
'''
from __future__ import division
import matplotlib
from pylab import *
from numpy import std
from numpy import mean
import matplotlib.axes
import matplotlib.pyplot as plt
 
class zscores(object):
    '''
    classdocs
    '''
    def draw(self, data = {}, z_score_key = ''):
       
        #Array mit Werten erstellen
        values = []
        site_values = []
        
        sites = data.keys()
        scores = data[data.keys()[0]].keys()
        z_scores = []
        
        for score in scores:
            #(raw score - mean of population) / standard deviation of population
            raw_score = data[z_score_key][score]
            
            for site in sites:
                site_values.append(data[site][score])
            
            mean_ = mean(site_values)
            std_ = std(site_values)
            
            z_score = (raw_score - mean_) / (std_)
            z_scores.append(z_score)
      
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        x_limit = max([max(z_scores), abs(min(z_scores))]) + 0.5
        xlim([-x_limit, x_limit])
        xlabel('Standard diviations (sigma)')
        ax.xaxis.grid(True)   
        
        yticks(arange(len(scores)), scores)
        ylim([0 - 0.5, len(scores) - 0.5])
        ax.yaxis.grid(False)
        
        ax.barh(arange(len(scores)), z_scores, height=0.2, align='center', color='black')
        
        show()

if __name__ == "__main__":
    data = {}
    sites = ["Facebook", "Google", "Microsoft", "IBM", "StudiVZ"]
    scores = ["Flesch", "RIX", "Dale-Chall", "SMOG"]
    
    for site in sites:
        data[site] = {}
        for score in scores:
            data[site][score] = rand()
      
    zs = zscores()
    zs.draw(data, "Facebook")