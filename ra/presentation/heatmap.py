'''
Created on 05.12.2011

@author: Marcus Voss
'''
import matplotlib
import matplotlib.pyplot as htmp_plot
from pylab import *
import scipy as scipy

class Heatmap(object):
    '''
    classdocs
    '''
    my_cmap = []
    def __init__(self):
        '''
        Constructor
        '''
        
        #eigene Colormap generieren, die von rot nach gruen variiert
        cdict = {'red':   
                    [(0.0,  0.0, 0.0),
                     (0.5, 1.0, 1.0),
                     (1.0,  1.0, 1.0)],
                'green': 
                   [(0.0,  1.0, 1.0),
                    (0.5, 1.0, 1.0),
                    (1.0,  0.0, 0.0)],
                'blue':  
                    [(0.0,  0.0, 0.0),
                     (0.5, 0.0, 0.0),
                     (1.0,  0.0, 0.0)]}
        self.my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        
    def create(self, data = {}):
       
        #Array mit Werten erstellen
        values = []
        site_values = []
        score_labels = []
        
        sites = data.keys()
        scores = data[data.keys()[0]]["scores"].keys()
        
        #exlude some scores that have not a grade level, so that they don't mess up colors
        for site in sites:
            for score in scores:
                if score <> "Flesch Reading Ease" and score <> "LIX" and score <> "RIX" and score <> "New Dale Chall" and score <> "New Dale Chall_enhanced":
                    site_values.append(data[site]["scores"][score])
                    score_labels.append(score)
            #append also the name of the site
            site_values.append(site)
            values.append(site_values)
            site_values = []
            
        #sort it according to flesch reading ease (values and labels)
        values = sorted(values, key=lambda flesch: flesch[0])
        #get only the numeric values
        score_values =  []
        #get the site names as labels
        y_labels = []
        for value in values:    
            score_values.append(value[:-1])
            y_labels.append(value[-1])
        #array with values to plot
        a = array(score_values)

        fig = htmp_plot.figure(figsize=(len(sites) * 2, len(scores) * 2))
      
        ax = fig.add_subplot(111)
        #ax.set_xticklabels(arange(len(scores)) + 0.5, score_labels, rotation=60)
        #figsize=(len(sites) * 1.5, len(scores) * 1.5)
        
        #Achsenbeschriftungen erstellen
        #htmp_plot.xticks( arange(len(scores)) + 0.5, score_labels, rotation=60)
        htmp_plot.yticks( arange(len(y_labels)) + 0.5, y_labels)
        
        #X-Achsenbeschriftung oben anzeigen und unten ausblenden
        for tick in gca().xaxis.iter_ticks():
            tick[0].label2On = True
            tick[0].label1On = False             
        
        xticks( arange(len(scores)) + 0.5, score_labels, rotation=10)
        
        #pcolor-Graph erzeugen
        htmp_plot.pcolor(a,cmap=self.my_cmap)
        
        #Legende erzeugen
        htmp_plot.colorbar()
        
        fig.autofmt_xdate()
        
    def draw(self, data):
        self.create(data)
        htmp_plot.show()
        
        
    def save(self, data, path="heatmap.png"):
        self.create(data)
        htmp_plot.savefig(path, format = 'png')

if __name__ == "__main__":
    #test dummy data    
    data = {}
    sites = ["Facebook", "Google", "Microsoft", "IBM", "StudiVZ"]
    scores = ["Flesch", "RIX", "Dale-Chall", "SMOG"]
    
    for site in sites:
        data[site] = {}
        data[site]["scores"] = {}
        for score in scores:
            data[site]["scores"][score] = rand()
      
    hm = Heatmap()
    hm.draw(data)
        