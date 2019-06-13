import json
import gensim
import os
import pickle
from gensim.models import Word2Vec
from gensim.models import FastText
from glove import Corpus, Glove


def main():

    # cl = pickle.load(open("EN_CommentList.p","rb"))
    cl = pickle.load(open("IT_CommentList.p","rb"))
    print("Making embeddings from: ",len(cl)," comments..")

    CommentList = []
    for comment in cl:
        comment.strip()
        words = comment.split(" ")
        CommentList.append(words)


    print("GloVe model.. ")
    corpus = Corpus()
    corpus.fit(CommentList, window=10)
    glove = Glove(no_components=100)
    glove.fit(corpus.matrix, epochs=30, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)
    glove.save('Italian_GloVe_embeddings.model')

    print("CBOW_default 1/4")
    model_CBOW = Word2Vec(CommentList, size=300, sg=0)
    print(model_CBOW)
    model_CBOW.save("CBOW_default_IT.model")
    print("-------")

    print("SKIP default 2/4")
    model_SKIP = Word2Vec(CommentList, size=300, sg=1)
    print(model_SKIP)
    model_SKIP.save("SKIP_default_IT.model")
    print("-------")

    print("SKIP n10 3/4")
    model_SKIP_n10 = Word2Vec(CommentList, size=300, sg=1, negative=10)
    print(model_SKIP_n10)
    model_SKIP_n10.save("SKIP_negative10_IT.model")
    print("-------")

    print("FastText 4/4")
    model_FastText = FastText(CommentList, size=300)
    print(model_FastText)
    model_FastText.save("FastText_default_IT.model")
    print("-------")

    print("done!")

main()
