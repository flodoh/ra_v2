'''
Created on 20.12.2011

@author: Marcus Voss
'''
from nltk_contrib.readabilitytests import *
from nltk_contrib.textanalyzer import *
from nltk.probability import FreqDist
from time import gmtime, strftime
import output.cheetah_output as co
import output_comparison.cheetah_output_comparison as co_comparison
from presentation.linechart import *
from presentation.dalechallgraph import *
from presentation.frychart import *
from presentation.heatmap import *
from database.db import *
#from input.input import *
#test vom 17.11.12
#test neuer branch
#test von flo
class ReadabilityAnalyzer(object):
    '''
    ##Testzeile fuer commit
    classdocs
    '''
    measures = []
    TEMPLATE_PATH = ''
    COMPARISON_TEMPLATE_PATH = ''
 
    def __init__(self):
        '''
        Constructor
        '''
        ##
        #measure available
        self.measures = ["ARI",
                         "Flesch Reading Ease",
                         "Flesch-Kincaid Grade Level",
                         "Gunning Fog Index",
                         "SMOG Index",
                         "Coleman Liau Index",
                         "LIX",
                         "RIX",
                         "New Dale Chall",
                         "New Dale Chall Grade",
                         'New Dale Chall_enhanced',
                         'New Dale Chall Grade_enhanced']
        
        #paths to the HTML templates
        self.TEMPLATE_PATH = '../output/html_output/'
        self.COMPARISON_TEMPLATE_PATH = '../output_comparison/html_output/'
        
    #generates scores for a text
    def get_measures(self, text, measures=''):
        site_dic = {}
        rt = ReadabilityTool(text)
        
        if measures == '':
            measures = self.measures
            
        # create for all defined measures the score with the help of Readability-Tool-Class  
        complete_site_dic = rt.get_test_scores(text)
        
        # write to site_dic only those calculated measures that are needed
        for measure in measures:
            site_dic[measure] = complete_site_dic[measure]
            
        return site_dic
        
    #returns all scores that are available
    def get_possible_measures(self):
        return self.measures

    #returns all names that are in the db and could be used as a key to work with
    def get_possible_names(self):
        get_all_names()
        return True
        
    #generates a report for a given text
      # ra.generate_report(data["Yahoo!"]["text"], "Yahoo!", data['Yahoo!']["url"])
    def generate_report(self, text, name='', url='', outputDirectory = '', save_db = False):
        data = {}
                
        if name == '':
            name = "some_site"
            
        call_name = name
            
        data[name] = {}
        
        #Measures
        data[name]["scores"] = self.get_measures(text)
        #Text
        data[name]["text"] = text
        #Meta-Daten
        data[name]["url"] = url
        if url == '':
            data[name]["url"] = '- no URL given -'       
        data[name]["name"] = call_name
        data[name]["date"] = strftime("%Y-%m-%d", gmtime())
       
        
        #Ordner fr Bilder erstellen (hochzaehlen wenn schon vorhanden
        #path = self.TEMPLATE_PATH + name + " 0001"outputDirectory
        path = outputDirectory + "/" + name + " 0001"
        
        i = 2
        while os.path.exists(path):
            path = path[:-4]
            path = path + '%04d' % i
            i = i + 1
        os.mkdir(path)
        
        #LinceChart erstellen
        lc = LineChart()
        line_path = path + "/" + "line_graph.png"
        lc.save(data[name]["scores"], line_path)
        data[name]["line_chart"] = line_path
        
        #Dale-Graph erstellen
        dalechall_path = path + "/" + "dalechall_graph.png"
        dcg = dalechallgraph()
        dcg.save(text, dalechall_path) 
        data[name]["dale_chall_graph"] = dalechall_path
        
        #Fry Graph erstellen
        fry_path = path + "/" + "fry_chart.png"
        fc = FryChart()
        fc.save(data, fry_path)
        data[name]["fry_graph"] = fry_path
               
        #save info into db
        if save_db == True:
            new_policy(name, text, url)
        
        co.create_report(data[name],outputDirectory)
        
        return True
    
    #creates the comparison report for several texts in data object
    def create_benchmark(self, data={}):

        #Ordner fr Bilder erstellen
        path = self.COMPARISON_TEMPLATE_PATH + "Report" + " 0001"
        i = 2
        #Endung hochzaehlen, bis ein Ordner erstellt werden kann, der noch nicht existiert
        while os.path.exists(path):
            path = path[:-4]
            path = path + '%04d' % i
            i = i + 1
        os.mkdir(path)
        
        # ADDED: Schreibt in den Typ dictionary fuer jede Seite (jede Policy) die entsprechenden Scores in ein neues Attribut "Scores" im Dictionary. Beispiel: Coleman Liau Index float: 8.09906103286
        for site in data:
            data[site]["scores"] = self.get_measures(data[site]["text"])
            
                                       
        #Fry Graph erstellen
        fry_path = path + "/" + "fry_chart.png"
        fc = FryChart()
        fc.save(data, fry_path)
        
        #Heatmap erstellen
        heat_path = path + "/" + "heatmap.png"
        hm = Heatmap()
        hm.save(data, heat_path)
        
        #comparison report aufrufen
        co_comparison.create_report(data, fry_path, heat_path)
        return True
    
    #creates comparison report for alle texts in the db
    def create_benchmark_from_db(self):
        data = {}
        data = get_all_policies()
        self.create_benchmark(data) 
        return True
    
    #creates single reports for each text in the db
    def create_all_reports_from_db(self, site_list = []):
        data = {}
        data = get_all_policies()
        
        for site in data:
            if site in site_list:
                self.generate_report(text = data[site]["text"], name= site, url = data[site]["url"], save_db = False)
        return True
        
    #creates a word list for the enhanced dale chall score - only needs to be called if not already produced
    def create_enhanced_dale_chall_list(self):
        #list of sites used to create list of most frequent words 
        alexa_list = ['Google', 'Facebook', 'YouTube', 'Yahoo!', 'Wikipedia', 'Microsoft', 'Amazon', 'Twitter', 'LinkedIn', 'Wordpress', 'Ebay', 'Apple', 'Paypal', 'Imdb', 'Tumblr', 'Disney', 'BBC', 'Livejasmin', 'Craigslist', 'Ask']
    
        #bring all privacy texts into one list
        corpus = []
        data = get_all_policies()
        for site in data:
                if site in alexa_list:
                    corpus.append(data[site]["text"])
        
        #get the words of this list into a list of words
        t = textanalyzer("eng")
        words = t.getWords("".join(corpus))
        
        #open the dale chall wordlist        
        dale_chall_list = open('../nltk_contrib/dale_chall_wordlist.txt').read().split(';')
        
        #create a text that consists of the words of the 20 privacy policies and delete all words that are on the dale-chall list of easy words
        new_corpus = []
        
        for word in words:
            if word.lower() not in dale_chall_list and word not in alexa_list:
                new_corpus.append(word.lower())
        
        #create a frequency distribution of the words of this list of words
        fdist = FreqDist(new_corpus)
        #plot this
        fdist.plot(80, cumulative=True)
        
        #make a list of the words that make up 33% percent of the words that are not in the dale chall list (cummulative)
        most_frequ = []
        cum_percentage = 0.0
        for sample in fdist:
            cum_percentage += fdist.freq(sample)
            most_frequ.append(sample)
            if cum_percentage > 0.33:
                break

        #write those into a file
        privacy_file = open("privacy_wordlist.txt", "w")
        privacy_file.write(";".join(most_frequ))
        

#Function to work with readabilityanalyzer:       
if __name__ == "__main__":
    ra = ReadabilityAnalyzer()
    
    #Different lists with keys from the DB to call reports with
    #List of privacy policies by google over the past 12 years
    google_list = ['Google_2012-03-01', 'Google_2011-10-20', 'Google_2010-10-03', 'Google_2009-03-11', 'Google_2009-01-27', 'Google_2008-08-07', 'Google_2005-10-14', 'Google_2004-07-01', 'Google_2000-08-14']
    
    #List of 20 popular sites of Alexa score
    alexa_list = ['Google_2012-03-01', 'Facebook', 'YouTube', 'Yahoo!', 'Wikipedia', 'Microsoft', 'Amazon', 'Twitter', 'LinkedIn', 'Wordpress', 'Ebay', 'Apple', 'Paypal', 'Imdb', 'Tumblr', 'Disney', 'BBC', 'Livejasmin', 'Craigslist', 'Ask']
    alexa_list_ext = ['Google_2012-03-01', 'Facebook', 'YouTube', 'Yahoo!', 'Wikipedia', 'Microsoft', 'Amazon', 'Twitter', 'LinkedIn', 'Wordpress', 'Ebay', 'Apple', 'Paypal', 'Imdb', 'Tumblr', 'Disney', 'BBC', 'BBC_update', 'Livejasmin', 'Craigslist', 'Ask', 'A CHRISTMAS TREE', 'Declaration of Independence', 'Bill of Rights', 'The giving tree']
   
    #List of easy and hard sites compared with children stories, the Bill of Rights and the Declaration of Independence
    easy_list = ['Google', 'Facebook', 'YouTube', 'Yahoo!', 'Wikipedia', 'Microsoft', 'Amazon', 'Twitter', 'Disney', 'BBC', 'A CHRISTMAS TREE', 'Declaration of Independence', 'Bill of Rights', 'The giving tree']
    easy_list2 = ['Google', 'Facebook', 'YouTube', 'Yahoo!', 'Wikipedia', 'Microsoft', 'Amazon', 'Twitter', 'Disney', 'BBC']
    easy_hard_list = ['Wordpress', 'Facebook', 'Disney', 'BBC', 'A CHRISTMAS TREE', 'Declaration of Independence', 'Bill of Rights', 'The giving tree', 'Wikipedia', 'Livejasmin']
    
    #choose list
    data = get_policies_by_names(alexa_list_ext)
    
    ra.create_benchmark(data)
    
    #for site in easy_hard_list:
    ra.generate_report(data["Yahoo!"]["text"], "Yahoo!", data['Yahoo!']["url"])
         
    a = 3
       
    
    
##################################################
#    Different calls to generate Data to Test functions:

#    fbtext = "Other information we receive about you We also receive other types of information about you: We receive data about you whenever you interact with Facebook, such as when you look at another person's profile, send someone a message, search for a friend or a Page, click on an ad, or purchase Facebook Credits. When you post things like photos or videos on Facebook, we may receive additional related data (or metadata), such as the time, date, and place you took the photo or video. We receive data from the computer, mobile phone or other device you use to access Facebook. This may include your IP address, location, the type of browser you use, or the pages you visit. For example, we may get your GPS location so we can tell you if any of your friends are nearby. We receive data whenever you visit a game, application, or website that uses Facebook Platform or visit a site with a Facebook feature (such as a social plugin). This may include the date and time you visit the site; the web address, or URL, you're on; technical information about the IP address, browser and the operating system you use; and, if you are logged in to Facebook, your User ID. Sometimes we get data from our advertising partners, customers and other third parties that helps us (or them) deliver ads, understand online activity, and generally make Facebook better. For example, an advertiser may tell us how you responded to an ad on Facebook or on another site in order to measure the effectiveness of - and improve the quality of - those ads. We also put together data from the information we already have about you and your friends. For example, we may put together data about you to determine which friends we should show you in your News Feed or suggest you tag in the photos you post. We may put together your current city with GPS and other location information we have about you to, for example, tell you and your friends about people or events nearby, or offer deals to you that you might be interested in. We may also put together data about you to serve you ads that might be more relevant to you. When we get your GPS location, we put it together with other location information we have about you (like your current city). But we only keep it until it is no longer useful to provide you services. We only provide data to our advertising partners or customers after we have removed your name or any other personally identifying information from it, or have combined it with other people's data in a way that it is no longer associated with you. Similarly, when we receive data about you from our advertising partners or customers, we keep the data for 180 days. After that, we combine the data with other people's data in a way that it is no longer 600 with you."
#    googletext = ''
#    ra.generate_report(fbtext, name="Facebook")
#    ra.generate_report(googletext, name="Google")
#    ra.get_measures(fbtext)
#    data = {}
#    data["Facebook"] = {}
#    data["Google"] = {}
#    data["Facebook"]["text"] = fbtext
#    data["Google"]["text"] = googletext
#    ra.create_benchmark(data)
###################################################

#    Call GUI:
#    input()

#    Call Functions to work with db:
#    ra.create_benchmark_from_db()  
#    ra.create_all_reports_from_db()
#    ra.create_report_from_db("Facebook")
#    ra.get_possible_names()
#    
#    ra.generate_report(gname, gtext, gurl)
#    ra.create_report(fbtext)