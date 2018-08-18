import gensim, nltk, re, json, os
from gensim import corpora,similarities, models
from nltk.tokenize import word_tokenize
from datetime import date,datetime
import csv 
import base64
from sklearn.cluster import k_means
import numpy as np

csv.field_size_limit(100000000)


data = []

with open('discursos_concatenados_2018.csv', 'r') as f:
    reader = csv.reader(f,delimiter=';')
    data = list(reader)
    colums = data.pop(0)

deputados_discursos = {}
body = []

for d in data:
    body.append(d[4])

stopwords = nltk.corpus.stopwords.words("portuguese")

regex = "[a-zA-ZçÇãÃõÕáÁéÉíÍóÓúÚâÂêÊîÎôÔûÛàÀ]+"

BASEDIR = os.getcwd()
if (os.path.exists(BASEDIR+"/discursos_dict.dict")):
   dictionary = corpora.Dictionary.load(BASEDIR+"/discursos_dict.dict")
   corpus = corpora.MmCorpus(BASEDIR+"/discursos_corpus.mm")
   lsi = models.LsiModel.load(BASEDIR+"/model_discursos.lsi")
else:
    documents_without_stopwords = [[w.lower() for w in word_tokenize(text) if w not in stopwords] 
                for text in body]
    documents = []
    for document in documents_without_stopwords:
        filtered_tokens = []
        for token in document:
            if re.search(regex, token):
                filtered_tokens.append(token)
        documents.append(filtered_tokens)
    from gensim.corpora import Dictionary
    from gensim.models import Word2Vec
    from gensim.similarities import SoftCosineSimilarity

    dictionary = corpora.Dictionary(documents)

    dictionary.save(BASEDIR+"/discursos_dict.dict")

    corpus = [dictionary.doc2bow(document) for document in documents]

    corpora.MmCorpus.serialize(BASEDIR+"/discursos_corpus.mm", corpus)

    tf_idf = models.TfidfModel(corpus)

    corpus_tfidf = tf_idf[corpus]

    lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=25)

    lsi.save(BASEDIR+"/model_discursos.lsi") 

index = similarities.Similarity(BASEDIR+"/index",lsi[corpus],num_features=len(dictionary),num_best=len(data))

with open("deputados.csv", 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["id", "nome", "partido", "idComparado","nomeComparado", "partidoComparado","pontuação"])
    for j in range(len(data)):
        vec_lsi = lsi[corpus_tfidf[j]]
        sims = index[vec_lsi]
        for s in sims:
            i = s[0]
            spamwriter.writerow([data[j][0],data[j][1], data[j][2], data[s[0]][0],data[s[0]][1],data[s[0]][2], s[1]])

