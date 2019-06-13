import json
import os
import string
from collections import defaultdict
import pickle

video_ID_list= []

k = defaultdict(int)

# store SenTube video IDs in pickle

for filename in os.listdir('automobiles_EN_extra_data'):
	filename  = 'automobiles_EN_extra_data/'+filename
	with open(filename) as json_data:
		d = json.load(json_data)
        video_ID_list.append(d["video_id"])

with open("automobiles_EN_extra_data_IDList.pickle", "wb") as listfile:
    pickle.dump(video_ID_list,listfile)

print(len(video_ID_list))