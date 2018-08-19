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

open_file('discursos_concat.csv',data)

body = []
for d in data:
    body.append(d[3])

stopwords = nltk.corpus.stopwords.words("portuguese")

regex = "[a-zA-ZçÇãÃõÕáÁéÉíÍóÓúÚâÂêÊîÎôÔûÛàÀ]+"

BASEDIR = os.getcwd()
# if (os.path.exists(BASEDIR+"/discursos_dict.dict")):
#    dictionary = corpora.Dictionary.load(BASEDIR+"/discursos_dict.dict")
#    corpus = corpora.MmCorpus(BASEDIR+"/discursos_corpus.mm")
#    lsi = models.LsiModel.load(BASEDIR+"/model_discursos.lsi")
# else:
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

dictionary.save(BASEDIR+"/discursos_dict.dict")

corpus = [dictionary.doc2bow(document) for document in documents]

corpora.MmCorpus.serialize(BASEDIR+"/discursos_corpus.mm", corpus)

tf_idf = models.TfidfModel(corpus)

corpus_tfidf = tf_idf[corpus]

lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary)

lsi.save(BASEDIR+"/model_discursos.lsi") 

index = similarities.Similarity(BASEDIR+"/index",lsi[corpus],num_features=len(dictionary),num_best=len(data))
with open("deputados.csv", 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["id", "nome", "partido", "idComparado","nomeComparado", "partidoComparado","pontuacao"])
    for j in range(len(data)):
        vec_lsi = lsi[corpus_tfidf[j]]
        sims = index[vec_lsi]
        for s in sims:
            i = s[0]
            spamwriter.writerow([j,data[j][0], data[j][1], i,data[s[0]][0],data[s[0]][1], s[1]])

topicos = [['lula','violência','mulher','petrobrás'],
['lula','golpe','petrobrás'],
['lula','educação'],
['lula','educação'],
['mulher','lula','violência','petrobrás'],
['consumidor','pesca'],
['pesca','rodovia'],
['feliciano','petrobrás','agricultura'],
['igreja','israel'],
['bolsonaro','policia','deus'],
['lula'],
['igreja','lula','eletrobrás'],
['igreja','pesca'],
['mulher','caminhoneiro','consumidor','agricultura'],
['igreja','petrobrás','consumidor'],
['esporte','turismo','pesca'],
['turismo','imigração','segurança'],
['turismo','pesca','imigração','esporte','segurança'],
['consumidor','mulher','pesca','segurança'],
['turismo','pesca','agricultura']
]
