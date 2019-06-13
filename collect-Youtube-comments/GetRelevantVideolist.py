from youtube_vid import youtube_search
import json
import csv 
import pickle
from langdetect import detect

data = []
addedIDlist = []


# Check language of the description and title 
def checkLanguage(description,title):
    try:
        if detect(description.decode('utf-8')) == 'it':
            return True
        else:
            return False
    except: 
        try:
            if detect(title.decode('utf-8')) == 'it':
                return True
            else:
                return False
        except:
            print("ERROR TO DETECT",description)
            return False

# Get IDs of videos in SenTube corpus
def getSentubeID():
    with open("SenTube_automobiles_IT_IDlist.pickle", "rb") as IDFile: 
        Idlist = pickle.load(IDFile)

    return(Idlist)

def grab_videos(keyword, token=None):
    res = youtube_search(keyword, token=token)
    token = res[0]
    videos = res[1]

    for vid in videos:
        video_dict = {}
        video_dict['youID']= vid['id']['videoId']
        
        vid_title = str("".join(vid['snippet']['title']).encode('utf-8').strip())
        video_dict['title'] = vid_title
        
        video_dict['pub_date'] = vid['snippet']['publishedAt']

        vid_description = str("".join(vid['snippet']['description']).encode('utf-8').strip())
        video_dict['video_description'] = vid_description

        vid_channelName = str("".join(vid['snippet']['channelTitle']).encode('utf-8').strip())
        video_dict['channel_name'] = vid_channelName

        vid_channelID = str("".join(vid['snippet']['channelId']).encode('utf-8').strip())
        video_dict['channelID'] = vid_channelID

        # Check if video not already in Sentube corpus and if decription is English
        Idlist = getSentubeID()
        if video_dict['youID'] not in Idlist:
            if video_dict['youID'] not in addedIDlist:
                if checkLanguage(vid_description,vid_title) == True:
                    data.append(video_dict)
                    addedIDlist.append(video_dict["youID"])              
        else:
            print(video_dict['youID'])

    print "added " + str(len(videos)) + " videos to a total of " + str(len(data))
    return token

def main():

    # search keywordlist
    keywordlist = ["recensione autovettura","recensione automobile","recensione auto"]

    for keyword in keywordlist:
        token = grab_videos(keyword)
        while token != "last_page":
            token = grab_videos(keyword, token=token)

    # Save videos in csv file 
    csv_columns = ['youID','title','pub_date','video_description','channel_name','channelID']

    with open("Automobiles_IT_searchlist.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for rows in data:
                writer.writerow(rows)
main()