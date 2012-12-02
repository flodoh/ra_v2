# coding=latin-1
'''
Created on 05.12.2011

@author: Marcus Voss
'''
from __future__ import division
import numpy as np
import matplotlib
import matplotlib.image as image
import matplotlib.pyplot as fry_plt
import matplotlib.axes as axes
from pylab import *
from nltk_contrib.textanalyzer import *

class FryChart(object):

    im = object
    
    def __init__(self):
        #Bild abgerufen von: http://en.wikipedia.org/wiki/File:Fry_Graph.png [zuletzt am 17.12.2011]
        #Bild steht unter der public domain - kann von daher fÃ¼r diese Zwecke genutzt werden
        #Bild ist in der Version: 14:11, 4 June 2010
        datafile = '../presentation/Fry_Graph.png'
        self.im = image.imread(datafile)
        
    def get_y_value(self, actual_value):
        #y-Achsen-werte gemÃ¤Ã des Fry Readability Graphes
        y_values = [2.0,2.5,3.0,3.3,3.5,3.6,3.7,3.8,4.0,4.2,4.3,4.5,4.8,5.0,5.2,5.6,5.9,6.3,6.7,7.1,7.7,8.3,9.1,10.0,11.1,12.5,14.3,16.7,20,25]
        
        #ist der Wert kleiner gleich 2, dann soll der Punkt auf der x-Achse liegen;
        #ist der Wert grÃ¶Ãer gleich 25, dann soll der Punkt auf am hÃ¶chst mÃ¶glichen Punkt liegen;
        #sonst wird der Wert (als NÃ¤herung) linear zwischen zwei Werten des Fry-Graphs interpoliert
        if actual_value <= y_values[0]:
            return 0
        elif actual_value >= y_values[len(y_values)-1]:
            return len(y_values)-1
        else:
            for i, v in enumerate(y_values):
                if actual_value <= y_values[i+1]:
                    return i + ((actual_value - y_values[i]) / (y_values[i + 1] - y_values[i]))
                
    def get_x_value(self, actual_value):
        if actual_value <= 108:
            return 108
        elif actual_value >= 174:
            return 174
        else: 
            return actual_value
                    
    def create(self, data = {}):
             
        sites = data.keys()
        
        ######################################
        # To calculate a grade level score:
        # 1. Randomly select three separate 100 word passages. 
        # 2. Count the number of sentences in each 100 word sample (estimate to nearest tenth).
        # 3. Count the number of syllables in each 100 word sample. (Each numeral is a syllable. For example, 2007 is 5 syllables -- two-thou-sand-se-ven -- and one word.)
        # 4. Plot the average sentence length and the average number of syllables on the graph.
        # The area in which it falls is the approximate grade
        ######################################
        
        for site in sites: 
            site_sentences = []
            site_words = []
            sentence_lengths = []
            
            sentences_count = []
            syllables_count = []
            
            ta = textanalyzer("eng")
            site_sentences = ta.getSentences(data[site]['text'])
            
            words = ta.getWords(data[site]['text'])
            word_count = len(words)
            
            for sentence in site_sentences:
                site_words.append(ta.getWords(sentence))
                sentence_lengths.append(len(ta.getWords(sentence)))
            
            sample_size = ""
            if word_count < 100:
                sample_size = word_count
                number_of_iterations = 1
            else:
                sample_size = 100
                if word_count < 200:
                    number_of_iterations = 1
                elif word_count < 300:
                    number_of_iterations = 2
                else:
                    number_of_iterations = 3
                
            j = 1
            
            while j <= number_of_iterations:
                count_index = j - 1
                
                if word_count < 100:
                    start = 0
                else:
                    start = randint(0, word_count - (sample_size * number_of_iterations))
                
                #Silben zaehlen
                sample_words = words[start:start + sample_size]
    
                #Sätze zaehlen
                
                #Beginn des Samples finden
                i = 0
                start_value = start
                while (start_value - sentence_lengths[i]) > 0:
                    start_value = start_value - sentence_lengths[i]
                    i += 1
            
                sentneces_count_rest = sentence_lengths[i] - start_value
                sentences_count.append(0.0)
                words_to_count_for = sample_size - sentneces_count_rest
                rest = sentneces_count_rest / sentence_lengths[i]
                
                #100 Wörter abzählen (abzüglich Restwörter aus Vorsatz)
                i += 1
                while (words_to_count_for - sentence_lengths[i]) > 0:
                    words_to_count_for = words_to_count_for - sentence_lengths[i]
                    sentences_count[count_index] = sentences_count[count_index] + 1
                    i += 1
                
                #Anzahl der Sätze zählen und Reste vorher und nachher aufaddieren
                sentences_count[count_index] = sentences_count[count_index]
                rest = rest + (words_to_count_for / sentence_lengths[i])
                
                #Werte vom aktuellen Sample
                sentences_count[count_index] = sentences_count[count_index] + rest
                syllables_count.append(ta.countSyllables(sample_words))
                
                #Wenn kleiner 100, dann auf 100 hochrechnen
                if word_count < 100:
                    sentences_count[count_index] = sentences_count[count_index] * 100 / word_count
                    syllables_count[count_index] = syllables_count[count_index] * 100 / word_count
                
                #das nächste sample
                j += 1
                
            data[site]['Syllables'] = float(sum(syllables_count)) / len(syllables_count)
            data[site]['Sentences'] = float(sum(sentences_count)) / len(sentences_count)
                      
        fig = fry_plt.figure(figsize=(8.15,5.03))
        
        ax = fig.add_subplot(111)
        
        #Achse ausblenden
        Axes.set_frame_on(ax, False)
        
        for site in sites:
            ax.plot(self.get_x_value(data[site]['Syllables']), self.get_y_value(data[site]['Sentences']), 'bo', ms=5)
            ax.annotate(site, (self.get_x_value(data[site]['Syllables']) - 6, self.get_y_value(data[site]['Sentences'])))

        fig.figimage(self.im, 82, 40)
     
        fry_plt.xlim([108, 174])
        fry_plt.xlabel("Average Number of Syllables per 100 words")
        fry_plt.xticks(arange(108, 174, 4))
        
        fry_plt.ylim([0,29])
        fry_plt.ylabel("Average Number of Sentences per 100 words")
        #Beschriftung gemÃ¤Ã Fry-Graph
        y_ticks = ['2.0','2.5','3.0','3.3','3.5','3.6','3.7','3.8','4.0','4.2','4.3','4.5','4.8','5.0','5.2','5.6','5.9','6.3','6.7','7.1','7.7','8.3','9.1','10.0','11.1','12.5','14.3','16.7','20','25+']
        fry_plt.yticks(arange(30), y_ticks)
        
        labels = sites
        
    def draw(self, data):
        self.create(data)
        fry_plt.show()
        
    def save(self, data, path="fry_chart.png"):
        self.create(data)
        fry_plt.savefig(path, dpi = 80, format = 'png')
        
if __name__ == "__main__":
    data = {}
    sites = ["Facebook", "Google"]
    
    text1 = "Other information we receive about you We also receive other types of information about you: We receive data about you whenever you interact with Facebook, such as when you look at another person's profile, send someone a message, search for a friend or a Page, click on an ad, or purchase Facebook Credits. When you post things like photos or videos on Facebook, we may receive additional related data (or metadata), such as the time, date, and place you took the photo or video."
        
    text2 = """Information you provide  When you sign up for a Google Account, we ask you for personal information. We may combine the information you submit under your account with information from other Google services or third parties in order to provide you with a better experience and to improve the quality of our services. For certain services, we may give you the opportunity to opt out of combining such information. You can use the Google Dashboard to learn more about the information associated with your Account. If you are using Google services in conjunction with your Google Apps Account, Google provides such services in conjunction with or on behalf of your domain administrator. Your administrator will have access to your account information including your email. Consult your domain administrators privacy policy for more information.
Cookies  When you visit Google, we send one or more cookies to your computer or other device. We use cookies to improve the quality of our service, including for storing user preferences, improving search results and ad selection, and tracking user trends, such as how people search. Google also uses cookies in its advertising services to help advertisers and publishers serve and manage ads across the web and on Google services.
Log information  When you access Google services via a browser, application or other client our servers automatically record certain information. These server logs may include information such as your web request, your interaction with a service, Internet Protocol address, browser type, browser language, the date and time of your request and one or more cookies that may uniquely identify your browser or your account.
User communications  When you send email or other communications to Google, we may retain those communications in order to process your inquiries, respond to your requests and improve our services. When you send and receive SMS messages to or from one of our services that provides SMS functionality, we may collect and maintain information associated with those messages, such as the phone number, the wireless carrier associated with the phone number, the content of the message, and the date and time of the transaction. We may use your email address to communicate with you about our services.
Affiliated Google Services on other sites  We offer some of our services on or through other web sites. Personal information that you provide to those sites may be sent to Google in order to deliver the service. We process such information under this Privacy Policy.
Third Party Applications  Google may make available third party applications, such as gadgets or extensions, through its services. The information collected by Google when you enable a third party application is processed under this Privacy Policy. Information collected by the third party application provider is governed by their privacy policies.
Location data  Google offers location-enabled services, such as Google Maps and Latitude. If you use those services, Google may receive information about your actual location (such as GPS signals sent by a mobile device) or information that can be used to approximate a location (such as a cell ID).
Unique application number  Certain services, such as Google Toolbar, include a unique application number that is not associated with your account or you. This number and information about your installation (e.g., operating system type, version number) may be sent to Google when you install or uninstall that service or when that service periodically contacts our servers (for example, to request automatic updates to the software).
Other sites  This Privacy Policy applies to Google services only. We do not exercise control over the sites displayed as search results, sites that include Google applications, products or services, or links from within our various services. These other sites may place their own cookies or other files on your computer, collect data or solicit personal information from you."""
       
    data["Facebook"] = {}   
    data["Facebook"]["text"] = text1
#    data["Google"] = {}
#    data["Google"]["text"] = text2
          
    fc = FryChart()
    fc.draw(data)
        