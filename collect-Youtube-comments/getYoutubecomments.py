from commentthreats import get_comment_threads
from commentthreats import get_comments
from apiclient.discovery import build
import pandas as pd 
import isodate
import pickle
import json


DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def getCategory(catnumber):
    with open("category_dict.pickle","rb") as categories:
        category_dict = pickle.load(categories)
        category = category_dict[catnumber]

    return category

def get_stats(videoId):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    stats = youtube.videos().list(part='statistics, snippet,contentDetails',id=videoId).execute()
    try:
        view_count = stats['items'][0]['statistics']['viewCount']
        catnumber = stats['items'][0]['snippet']['categoryId']
        category = getCategory(catnumber)
        duration = stats['items'][0]['contentDetails']['duration']
        dur = isodate.parse_duration(duration).total_seconds()
    except:
        view_count = ""
        category = ""
        dur = ""

    return view_count,category,dur 

def load_comments(match):
    
    for item in match["items"]:

        comment_dict = {}

        vid_comment = str("".join(item['snippet']['topLevelComment']).encode('utf-8').strip())
        comment_int = item['snippet']['topLevelComment']

        text = str("".join(comment_int['snippet']['textDisplay']).encode('utf-8').strip())
        comment_dict["text"] = text

        com_published = comment_int["snippet"]["publishedAt"]
        comment_dict["published"] = com_published

        commentID = comment_int["id"]
        comment_dict["id"] = commentID

        com_author = str("".join(comment_int["snippet"]["authorDisplayName"]).encode('utf-8').strip())
        comment_dict["author"] = com_author

        comment_dict["annotation"] = ""

        comments.append(comment_dict)

        #print "added " + str(len(match["items"])) + " comments to a total of " + str(len(comments))

def main():
    # Read CSV file with videos
    print "Reading in file.."
    # df = pd.read_csv("automobiles_commercial_EN_searchlist.csv")
    # df = pd.read_csv("searchlists/automobiles_commercial_IT_searchlist.csv")
    df = pd.read_csv("searchlists/tablets_commercial_IT_searchlist.csv")
    count = 0
    amountcomments = 0 

    # For every video in the videolist
    for index, row in df.iterrows():
        comments = []

        # Get the Id, title, uploader,published, and extra stats (view_count, category,duration)
        video_id = row['youID']
        title = row['title']
        uploader = row['channel_name']
        video_description = row['video_description']
        published = row['pub_date']
        view_count,category,duration = get_stats(video_id)


        #Get commentlist
        try:
            match = get_comment_threads(video_id,token=None)
            load_comments(match)
            try:
                next_page_token = match["nextPageToken"]
                while next_page_token:
                    match = get_comment_threads(video_id,token=next_page_token)
                    load_comments(match)
                    next_page_token = match["nextPageToken"]
            except:
                pass
        except:
            pass

        if len(comments) >= 1:
            # make dictionary to write Json
            video_dict = {}
            video_dict["category"] = category
            video_dict["view_count"] = view_count
            video_dict["video_description"] = video_description
            video_dict["title"] = title
            video_dict["avg_rating"] = ""
            video_dict["video_id"] = video_id
            video_dict["comments"] = comments
            video_dict["uploader"] = uploader
            video_dict["published"] = published
            video_dict["duration"] = duration

            filename = "tablets_IT_commercial_data/video_"+video_id+".json"
            with open(filename,"wb") as jsonfile:
                 json.dump(video_dict,jsonfile)
            
            # print feedback
            count = count + 1
            amountcomments = amountcomments + len(comments)
            print "Stored ",video_id, "in tablets_IT_commercial_data with\t",len(comments),"comments. \t Total videos stored: ",count 

    print "total amount of comments: ",amountcomments

main()


