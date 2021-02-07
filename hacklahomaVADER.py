import twint
import re
import demoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


numtweets = 300 # number of tweets we are pulling for each search term

#   SentimentFinder finds the sentiment of a Tweets from a certain time on certain key words. In our case
#   we are finding current sentiment and yesterday's sentiment on "must", "elon must", and " tesla" which
#   are have a significant coorelation with $TSLA
class SentimentFinder(object):
    
    #   twitter_scrape populates text files with tweets with key words from a certain day 
    def twitter_scrape(self):
        t = twint.Config()  
        t.Limit = numtweets

        t.Until = "2021-02-06"

        t.Search = "musk"
        t.Store_object = True
        t.Output = "test1.txt"
        twint.run.Search(t)


        t.Search = "elon musk"
        t.Output = "test2.txt"
        twint.run.Search(t)

        t.Search = "tesla"
        t.Output = "test3.txt"
        twint.run.Search(t)

        t.Until = "2021-02-05"

        t.Search = "musk"
        t.Output = "testyesterday1.txt"
        twint.run.Search(t)

        t.Search = "elon musk"
        t.Output = "testyesterday2.txt"
        twint.run.Search(t)

        t.Search = "tesla"
        t.Output = "testyesterday3.txt"
        twint.run.Search(t)

    
        
    #   find_polarity cleans the tweets from excess symbols and links, then analyzes the sentiment to 
    #   find the polarity of the sentiment
    def find_polarity(self, textfile):
        polarity = 0.0
        with open(textfile, encoding="utf8") as f:
            fl = f.readlines()
        clean_line = ""
        for x in range(numtweets):
            p = fl[x].split(">",1)
            clean_line = demoji.replace(p[1], " ")
            clean_line = ' '.join(re.sub("([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", " ", clean_line).split())
            clean_line = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)", " ", clean_line).split())
            print(clean_line)
            analyzer = SentimentIntensityAnalyzer()
            full_polarity = analyzer.polarity_scores(clean_line) 
            polarity += full_polarity['compound']

        return polarity



def main():
    
    #populates the text files
    twit_obj = SentimentFinder()
    twit_obj.twitter_scrape()

    #finds and sums the polarity of the tweets
    polarity = twit_obj.find_polarity("test1.txt")
    open("test1.txt", 'w').close()

    polarity += twit_obj.find_polarity("test2.txt")
    open("test2.txt", 'w').close()

    polarity += twit_obj.find_polarity("test3.txt")
    open("test3.txt", 'w').close()

    lastpolarity = twit_obj.find_polarity("testyesterday1.txt")
    open("testyesterday1.txt", 'w').close()

    lastpolarity += twit_obj.find_polarity("testyesterday2.txt")
    open("testyesterday2.txt", 'w').close()

    lastpolarity += twit_obj.find_polarity("testyesterday3.txt")
    open("testyesterday3.txt", 'w').close()

    #averages the polarites
    average = polarity/(numtweets*3)
    lastaverage = lastpolarity/(numtweets*3)

    #for presentation purposes only
    print ("current sentiment: ")
    print (average)
    print ("last sentiment: ")
    print (lastaverage)

    #compares averages and prints prediction
    if (average > lastaverage):
        print("Prediction: $TSLA is on the rise")
    elif (average < lastaverage):
        print("Prediction: $TSLA is on the fall")
    else:
        print("Prediction: $TSLA is going to stay about the same")

    
if __name__ == "__main__": 
 	# calling main function 
 	main() 