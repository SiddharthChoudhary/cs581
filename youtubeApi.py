from apiclient.discovery import build
import csv
import argparse
import ssl
import csv
import unidecode

API_KEY = 'AIzaSyDHn1n3QDMpQZSgYeUQSdngwyVXJzcqtKk'
API_NAME = 'API key 1'
API_VERSION= 'v3'

parser = argparse.ArgumentParser(description='Youtube Search')
parser.add_argument("--search_term",default="music")
parser.add_argument("--search_max",default=30)
args = parser.parse_args()
def youtube_search_engine(args):
        youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
        searchResponse = youtube.search().list(q=args.search_term,part="id,snippet",
                                                maxResults=args.search_max).execute()
        csvFile = open('video_results.csv','w')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(["TITLE","ID","VIEWS","LIKES","DISLIKES","COMMENTS","FAVORITES"])
        csvFile.close()
youtube_search_engine(args)