import json
import gensim
import os
import pickle

def getAllComments(directoryfileslist):
    Allcomments = []
    for dirfile in directoryfileslist:
        print("collecting comments from: ",dirfile)    
        for filename in os.listdir(dirfile):
            with open(dirfile+"/"+filename) as json_data:
                d = json.load(json_data)
                for comment in d["comments"]:
                    lower = comment["text"].lower().strip()
                    Allcomments.append(lower)
    return Allcomments   



def main():
    tablets_automobiles = ["tablets_IT_extra_data","automobiles_IT_extra_data"]
    Allcommentlist = getAllComments(tablets_automobiles)
    print("collected Allcomments")
    print(Allcommentlist[10])

    print("SavingCommentlist..")
    pickle.dump(Allcommentlist, open("IT_CommentList.p","wb"))
    print("comments saved at: IT_CommentList.p" )
main()