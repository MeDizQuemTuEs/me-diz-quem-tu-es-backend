import gensim, nltk, re, json, os
from gensim import corpora,similarities, models
from nltk.tokenize import word_tokenize
from datetime import date,datetime
import csv 
import base64
from sklearn.cluster import k_means
import numpy as np
csv.field_size_limit(100000000)

def open_file(name_file,data):
    with open(name_file,'r') as f:
        reader = csv.reader(f,delimiter=';')
        lista_por_arquivo = list(reader)
        lista_por_arquivo.pop(0)
        data +=  lista_por_arquivo

data = []

open_file('discursos_sep.csv',data)

body = []
for d in data:
    body.append(d[5])

stopwords = nltk.corpus.stopwords.words("portuguese")

regex = "[a-zA-ZçÇãÃõÕáÁéÉíÍóÓúÚâÂêÊîÎôÔûÛàÀ]+"

BASEDIR = os.getcwd()

documents_without_stopwords = [[w.lower() for w in word_tokenize(text) if w not in stopwords] 
            for text in body]
    
documents = []
for document in documents_without_stopwords:
    filtered_tokens = []
    for token in document:
        if re.search(regex, token):
            filtered_tokens.append(token)
    documents.append(filtered_tokens)

dictionary = corpora.Dictionary(documents)
corpus = [dictionary.doc2bow(document) for document in documents]
tf_idf = models.TfidfModel(corpus)
corpus_tfidf = tf_idf[corpus]
lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=20)
index = similarities.Similarity(BASEDIR+"/index",lsi[corpus],num_features=len(dictionary),num_best=len(data))
with open("result_discurso__sep.csv", 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["id","idCoparado","pontuacao"])
    for j in range(len(data)):
        vec_lsi = lsi[corpus_tfidf[j]]
        sims = index[vec_lsi]
        if (len(vec_lsi)>0):
            for k in range(5):
                i = sims[k][0]
                spamwriter.writerow([data[j][0], i, sims[k][1]])