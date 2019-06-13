import json
import os
import string
from collections import defaultdict
import pickle
import random
import csv

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# select 50 random comment from each category to check manually 

commentdict = {}
data = []
items = []

directory = "Extra_datasets_withoutNaN"
# category = "automobiles_EN_extra_data"
category = "tablets_EN_extra_data"

print "making dict of all comments ..."
for filename in os.listdir(directory+"/"+category):
	filename  = directory+"/"+category+"/"+filename
	with open(filename) as json_data:
		d = json.load(json_data)
        for comment in d['comments']:
            commentlist = []
            commentlist.append(d["video_id"])
            commentlist.append(d["video_description"])
            commentlist.append(d["title"])
            commentlist.append(comment["text"])
            commentdict[comment["id"]] = commentlist

print "selecting 50 comments random..."

while len(items) < 50:
    random_item = random.choice(list(commentdict))
    if random_item in items:
        pass
    else:
        items.append(random_item)
        randomSample = {}
        video_id,video_description,title,commenttext = commentdict[random_item]
        randomSample["comment_ID"] = random_item.encode('utf-8')
        randomSample["video_id"] = video_id.encode('utf-8')
        randomSample["video_description"] = video_description.encode('utf-8')
        randomSample["video_title"] = title.encode('utf-8')
        randomSample["comment"] = commenttext.encode('utf-8')
        data.append(randomSample)



print "writing sample to csv.."
csv_columns = ['comment_ID','video_id','video_description','video_title','comment']

with open("RandomSamples/tablets_EN_RandomSample.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns,dialect='excel-tab')
        writer.writeheader()
        for rows in data:
            writer.writerow(rows)

# with open("Automobiles_EN_RandomSample.pickle", "wb") as listfile:
#     pickle.dump(randomSamples,listfile)


# comments = []

# for key in randomSamples:
#     video_id,video_description,title,commenttext = randomSamples[key]
#     comments.append(commenttext)