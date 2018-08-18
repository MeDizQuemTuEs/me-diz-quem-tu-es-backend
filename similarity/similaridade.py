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
    body.append(d[2])

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

    dictionary = corpora.Dictionary(documents)

    dictionary.save(BASEDIR+"/discursos_dict.dict")

    corpus = [dictionary.doc2bow(document) for document in documents]

    corpora.MmCorpus.serialize(BASEDIR+"/discursos_corpus.mm", corpus)

    tf_idf = models.TfidfModel(corpus)
    tf_idf.save(BASEDIR+"/tf_idf_model_discursos.mm")
    corpus_tfidf = tf_idf[corpus]

    lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=300)

    lsi.save(BASEDIR+"/model_discursos.lsi") 

index = similarities.Similarity(BASEDIR+"/index",lsi[corpus],num_features=len(dictionary),num_best=len(data))
vec_lsi = lsi[corpus_tfidf[0]]
sims = index[vec_lsi]

# from gensim.corpora import Dictionary
# from gensim.models import Word2Vec
# from gensim.similarities import SoftCosineSimilarity
# model = Word2Vec(documents, size=20, min_count=1)  # train word-vectors
# dictionary = Dictionary(documents)
# bow_corpus = [dictionary.doc2bow(document) for document in documents]
# similarity_matrix = model.wv.similarity_matrix(dictionary)  # construct similarity matrix
# index = SoftCosineSimilarity(bow_corpus, similarity_matrix, num_best=10)
# # Make a query.
# query = 'graph trees computer'.split()
