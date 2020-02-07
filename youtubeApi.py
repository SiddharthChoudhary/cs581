# Author:  SIDDHARTH CHOUDHARY#  
# youtubeApi.py searches YouTube for videos matching a search term
# #  It writes info for each video, up to a specified maximum number, to a .csv file
# # to run from terminal window:  
# #      python3 youtubeApi.py --search_term mysearch --search_max mymaxresults# 
#  where:  search_term = the term you want to search for;  default = music#    
#  and  search_max = the maximum number of results;  default = 30

#The output contains the best liked videos out of that search which we are printing on the screen

from apiclient.discovery import build      
from subprocess import check_output, CalledProcessError,STDOUT
import ssl,json
import argparse   
import csv         
import unidecode   

#This module focuses on checking the ssl error and then handling it later
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

#  API key into the API_KEY field below, in quotes
API_KEY = "AIzaSyDHn1n3QDMpQZSgYeUQSdngwyVXJzcqtKk"
API_NAME = "youtube"     #this should always be youtube
API_VERSION = "v3"       # this should be the latest version
#  function youtube_search retrieves the YouTube records
def youtube_search(options):
    try:
        youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
        search_response      = youtube.search().list(q=options.search_term, part="id,snippet", maxResults=options.search_max).execute()
    except AttributeError:
        url = "https://www.googleapis.com/youtube/v3/search?maxResults="+options.search_max+"&key="+API_KEY+"&part=id,snippet"
        search_response      = check_output(["curl",url,"--fail","--silent","--header","'Accept:application/json'","--compressed"],stderr=STDOUT).decode()
        search_response      = json.loads(search_response)
    
    # This handles bestLikeCounts which handles a dictionary to calculate the maximum number of likes
    bestLikeCounts = {}
    maximum = 0
    maximumTitle = ''
    csvFile = open('video_results.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["TITLE","ID","VIEWS","ACTUAL LIKES"])
    try:
        # search for videos matching search term; write an output line for each
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                title = search_result["snippet"]["title"]
                title = unidecode.unidecode(title)  
                videoId = search_result["id"]["videoId"]
                #traversing the each video content in a particular object
                video_response = youtube.videos().list(id=videoId,part="statistics").execute()
                for video_results in video_response.get("items",[]):
                    viewCount = video_results["statistics"]["viewCount"]
                    if 'likeCount' not in video_results["statistics"]:
                        likeCount = 0
                    else:
                        likeCount = video_results["statistics"]["likeCount"]
                    if 'dislikeCount' not in video_results["statistics"]:
                        dislikeCount = 0
                    else:
                        dislikeCount = video_results["statistics"]["dislikeCount"]
                likeCount=int(likeCount)
                dislikeCount=int(dislikeCount)
                bestLikeCounts[title]=likeCount
                #calculating the actual likes by removing dislikes from likes
                if likeCount>dislikeCount:
                    actualCount=likeCount-dislikeCount
                else:
                    actualCount=dislikeCount-likeCount
                for key in bestLikeCounts:
                    if(bestLikeCounts[key]>maximum):
                        maximum=bestLikeCounts[key]
                        maximumTitle=key
                #writing the output in the end to the file
                csvWriter.writerow([title,videoId,viewCount,actualCount])
        print("!!Your CSV file is ready!! and should be in the current directory named after video_results.csv")
        print("\n\n The best video being liked among the search is '",maximumTitle,"' with likes as follows: ",maximum)
    except Exception as e:
        print("Couldn't write to the CSV due to error ",e)
    csvFile.close()
  
# main routine
print("WELCOME TO OUR ACTUAL YOUTUBE API TRAVERSAL\n")
print("We are actually calculating the actual number of people who really liked your video and on which you can rely\n")
print("Note: We calculate this by differentiating between those who liked and those who disliked\n\n")
print("Now we are processing your request!! Hold tight and be ready to check the CSV file\n\n")
parser = argparse.ArgumentParser(description='YouTube Search')
parser.add_argument("--search_term", default="music")
parser.add_argument("--search_max", default=30)
args = parser.parse_args()
#the main function to be called
youtube_search(args)
