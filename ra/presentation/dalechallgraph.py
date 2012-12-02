'''
Created on 06.12.2011

@author: Marcus Voss
'''
import matplotlib
import matplotlib.pyplot as dale_plt
from pylab import *
from nltk_contrib.readabilitytests import *
from nltk_contrib.textanalyzer import *

class dalechallgraph(object):
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
                     (0.25, 0.8, 0.8),
                     (0.75, 1.0, 1.0),
                     (1.0,  1.0, 1.0)],
                'green': 
                   [(0.0,  0.0, 0.0),
                    (0.25, 0.8, 0.8),
                    (0.75, 0.0, 0.0),
                    (1.0, 1.0, 1.0)],
                'blue':  
                    [(0.0,  0.0, 0.0),
                     (0.25, 0.8, 0.8),
                     (0.75, 0.0, 0.0),
                     (1.0,  1.0, 1.0)]}
        self.my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        
    def create(self, text = ''):
       
        #rfi = readabilityFilesInstaller()
       # NewDaleChallWordsFile = open(rfi.getPath("Dale-Chall wordlist")[0]).read()
      #  NewDaleChallWordsList = NewDaleChallWordsFile.split(';')
        
        #Array mit Werten erstellen
        ta = textanalyzer("eng")
        raw_sentences = ta.getSentences(text)
        
        values = []
        sentence_values = []
        max_words = 0
        for sentence in raw_sentences:
            raw_words = ta.getWords(sentence)
            if len(raw_words) > max_words:
                max_words = len(raw_words)
            for word in raw_words:
                value = 0.0
             #   if word.lower() in NewDaleChallWordsList: 
            #        value = 0.25
             #   else:
            #        value = 0.5
                 
                if word.isdigit():
                    value = 0.0   
                sentence_values.append(value)
            values.append(sentence_values)   
            sentence_values = []
        
        #mit Nullen auffuellen
        for value in values:
            while len(value) < max_words:
                value.append(1.0)
        
        values.reverse()        
        a = array(values)
        
        fig = dale_plt.figure()
            
        #Achsenbeschriftungen erstellen
        
        i = len(values)
        ylabels = []
        while i > 0:
            ylabels.append(i)
            i = i - 1

        yticks( arange(len(values))+0.5, ylabels  )
               
        #pcolor-Graph erzeugen
        pcolor(a,cmap=self.my_cmap, norm=normalize(vmin=0.0, vmax=1.0))
        
        #Legende erzeugen
        #colorbar()
    
    def draw(self, text): 
        self.create(text)  
        show() 
        
    def save(self, text, path='dale_chall.png'):
        self.create(text)  
        savefig(path, format = 'png')

if __name__ == "__main__":
    
    text = "Other information we receive about you We also receive other types of information about you: We receive data about you whenever you interact with Facebook, such as when you look at another person's profile, send someone a message, search for a friend or a Page, click on an ad, or purchase Facebook Credits. When you post things like photos or videos on Facebook, we may receive additional related data (or metadata), such as the time, date, and place you took the photo or video. We receive data from the computer, mobile phone or other device you use to access Facebook. This may include your IP address, location, the type of browser you use, or the pages you visit. For example, we may get your GPS location so we can tell you if any of your friends are nearby. We receive data whenever you visit a game, application, or website that uses Facebook Platform or visit a site with a Facebook feature (such as a social plugin). This may include the date and time you visit the site; the web address, or URL, you're on; technical information about the IP address, browser and the operating system you use; and, if you are logged in to Facebook, your User ID. Sometimes we get data from our advertising partners, customers and other third parties that helps us (or them) deliver ads, understand online activity, and generally make Facebook better. For example, an advertiser may tell us how you responded to an ad on Facebook or on another site in order to measure the effectiveness of - and improve the quality of - those ads. We also put together data from the information we already have about you and your friends. For example, we may put together data about you to determine which friends we should show you in your News Feed or suggest you tag in the photos you post. We may put together your current city with GPS and other location information we have about you to, for example, tell you and your friends about people or events nearby, or offer deals to you that you might be interested in. We may also put together data about you to serve you ads that might be more relevant to you. When we get your GPS location, we put it together with other location information we have about you (like your current city). But we only keep it until it is no longer useful to provide you services. We only provide data to our advertising partners or customers after we have removed your name or any other personally identifying information from it, or have combined it with other people's data in a way that it is no longer associated with you. Similarly, when we receive data about you from our advertising partners or customers, we keep the data for 180 days. After that, we combine the data with other people's data in a way that it is no longer 600 with you."
          
    dcg = dalechallgraph()
    dcg.draw(text)
    #dcg.save(text)