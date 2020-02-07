#  Author:  Siddharth Choudhary

# twitter_data_analysis.py searches Twitter for tweets matching the search terms,
#      up to a maximun number being passed through command line. By default it's 30

######  user must supply authentication keys where indicated

# to run from terminal window: 

#        run: 
#           $pip install -r requirements.txt
#        Also if you face nltk error then we need to run:
#           python -m textblob.download_corpora

#       then:
#        python3  twitter_data_analysis.py   --search_term1  mysearch  --search_term2 mysearch2 --search_max  mymaxresults 
#           where:  mysearch1 and mysearch2 are the terms the user wants to search for;  default = music and soccer
#            and:  mymaxresults is the maximum number of resulta;  default = 30

# Here we are hitting the twitter twice by using two search terms 

# The program uses the TextBlob sentiment property to analyze the tweet for:
#  1. I am using textblob's summarization to generate summary
#  2. also using the language detection to detect what is the language of the following text
#  3. and am using the spelling correction feature to correct the spelling of the text

# The program creates a .csv output file with a line for each tweet
#    including tweet data items and the sentiment information

from textblob import TextBlob,Word	# needed to analyze text for sentiment
import argparse    				# for parsing the arguments in the command line
import csv						# for creating output .csv file
import tweepy					# Python twitter API package
import unidecode				# for processing text fields in the search results
import random

### PUT AUTHENTICATOIN KEYS HERE ###
CONSUMER_KEY = "X2jP02YKrk5vk41tUWYW6Bndm"
CONSUMER_KEY_SECRET = "t4r183HpkTwWVk3RA9myd3FWsWMUIPTxYXtyCsbUBqSrFqtoVs"
ACCESS_TOKEN = "2360592954-ithoJHJSEwgEtLbvOXN1p116Ylzk5lEN2oPbknQ"
ACCESS_TOKEN_SECRET = "q0xUpkSFn8vivxAJloy8tX4P8OuBCkicE36U7Z9So19v5"

# AUTHENTICATION (OAuth)
authenticate = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(authenticate)


#this function generates the summary of the context using tags to find out the nouns in the text and then later generating a summary of it
def create_summary(text):
    blob=TextBlob(text)
    summary=[]
    nouns=list()
    #first find the tags from the blob and then lemmatize the text
    for word,tag in blob.tags:
        if tag=='NN':
            nouns.append(word.lemmatize())
    if len(nouns)>0:
        for item in random.sample(nouns, len(nouns)):
            word = Word(item)
            summary.append(word.pluralize())
    return summary
#This function the writes the row in csv based on the search_Terms and search_maxs passed to it.
def write_in_csv(csvWriter,search_term,search_max):
    for tweet in tweepy.Cursor(api.search, q = search_term, result_type = "popular").items(search_max):    
        created = tweet.created_at                       # date created    
        text = tweet.text                               # text of the tweet
        text = unidecode.unidecode(text)
        retweets = tweet.retweet_count             # number of retweets    
        username  = tweet.user.name                # user name    
        userid  = tweet.user.id                     # userid    
        followers = tweet.user.followers_count      # number of user followers 
        if text:
            blob=TextBlob(text)
            #get correct spelled text
            correct_spelled_text=blob.correct()
            #get summary of the text in an array form, counting all the nouns
            summary=create_summary(text)
            #and detect the language
            language=blob.detect_language()
        csvWriter.writerow([created,text,retweets,username,userid,followers,correct_spelled_text,summary,language])


# Get the input arguments - search_term and search_max
parser = argparse.ArgumentParser(description='Twitter Search')

parser.add_argument("--search_term1", action='store', dest='search_term1', default="music")
parser.add_argument("--search_term2", action='store', dest='search_term2', default="soccer")
parser.add_argument("--search_max", action='store', dest='search_max', default=30)

args = parser.parse_args()

search_term1 = args.search_term1
search_term2 = args.search_term2
search_max = int(args.search_max)

#calling the main function by opening the csv file and writing in it
csvFile = open('twitter_results.csv','w')
csvWriter = csv.writer(csvFile)
print("parsing.... Wait !!!")
csvWriter.writerow(['Date_Created','Tweet',"Retweets_Count","Username","Userid","Followers","Correct_Spelled_Tweet","Summary_Tweet","Language_Of_Tweet"])
write_in_csv(csvWriter,search_term1,search_max)
write_in_csv(csvWriter,search_term2,search_max)
print("File is generated. Your welcome")
csvFile.close()