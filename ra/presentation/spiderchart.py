'''
Created on 05.12.2011

@author: Marcus Voss
'''
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection

from pylab import *

class SpiderChart(object):
    
    def draw(self, data, frame='circle'):
        """Create a radar chart with `num_vars` axes."""
        values = []
        site_values = []
            
        sites = data.keys()
        scores = data[data.keys()[0]].keys()
            
        for site in sites:
            for score in scores:
                site_values.append(data[site][score])
            values.append(site_values)
            site_values = []
            
        num_vars = len(scores)   
        
        # calculate evenly-spaced axis angles
        theta = 2*np.pi * np.linspace(0, 1-1./num_vars, num_vars)
        # rotate theta such that the first axis is at the top
        theta += np.pi/2
    
        class RadarChart(PolarAxes):
            """Class for creating a radar chart (a.k.a. a spider or star chart)
    
            http://en.wikipedia.org/wiki/Radar_chart
            """
            name = 'radar'
            # use 1 line segment to connect specified points
            RESOLUTION = 1
            
            def draw_circle_frame(self, x0, y0, r):
                return plt.Circle((x0, y0), r)
               
            def fill(self, *args, **kwargs):
                """Override fill so that line is closed by default"""
                closed = kwargs.pop('closed', True)
                return super(RadarChart, self).fill(closed=closed, *args, **kwargs)
    
            def plot(self, *args, **kwargs):
                """Override plot so that line is closed by default"""
                lines = super(RadarChart, self).plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)
    
            def _close_line(self, line):
                x, y = line.get_data()
                # FIXME: markers at x[0], y[0] get doubled-up
                if x[0] != x[-1]:
                    x = np.concatenate((x, [x[0]]))
                    y = np.concatenate((y, [y[0]]))
                    line.set_data(x, y)
    
            def set_varlabels(self, labels):
                self.set_thetagrids(theta * 180/np.pi, labels)
    
            def _gen_axes_patch(self):
                x0, y0 = (0.5, 0.5)
                r = 0.5
                return self.draw_circle_frame(x0, y0, r)
    
        register_projection(RadarChart)

        fig = plt.figure(figsize=(9,9))
        
        #TODO: wenn mehr als 5 sites!!! Rais exception?? Gemerate more colors??
        colors = ['b', 'r', 'g', 'm', 'y']
        ax = fig.add_subplot(1,1, 1, projection='radar')
        plt.rgrids([0.2, 0.4, 0.6, 0.8])
        
        for d, color in zip(values, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(scores)      
        
        # add legend relative to top-left plot
        labels = sites
        plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
    
        plt.show()
       
if __name__ == '__main__':
   
    data = {}
    sites = ["Facebook", "Google", "Microsoft", "IBM", "StudiVZ"]
    scores = ["Flesch", "RIX", "Dale-Chall", "SMOG", "Test"]
    
    for site in sites:
        data[site] = {}
        for score in scores:
            data[site][score] = rand()
            
    sc = SpiderChart()
    sc.draw(data)