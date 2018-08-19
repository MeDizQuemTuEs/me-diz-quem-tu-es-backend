import gensim, nltk, re, json, os
from gensim import corpora,similarities, models
from nltk.tokenize import word_tokenize
from datetime import date,datetime
import csv 
import base64
from sklearn.cluster import k_means
import numpy as np
import unicodedata
from nltk.stem.snowball import SnowballStemmer

BASEDIR = os.getcwd()

if (os.path.exists(BASEDIR+"/discursos_corpus.mm")):
   dictionary = corpora.Dictionary.load(BASEDIR+"/discursos_dict.dict")
   corpus = corpora.MmCorpus(BASEDIR+"/discursos_corpus.mm")

else:
    def remover_combinantes(string):
        string = unicodedata.normalize('NFD', string)
        return u''.join(ch for ch in string if unicodedata.category(ch) != 'Mn')

    stemmer = SnowballStemmer("portuguese")

    csv.field_size_limit(100000000)

    estadosBrasileirosStem  = []
    with open('stop_words.csv','r') as f:
        reader = csv.reader(f)
        estadosBrasileirosStem = list(reader)[0]
    for i in range(len(estadosBrasileirosStem)):
        estadosBrasileirosStem[i] = stemmer.stem(remover_combinantes(estadosBrasileirosStem[i]))

    def open_file(name_file,data):
        with open(name_file,'r') as f:
            reader = csv.reader(f,delimiter=';')
            lista_por_arquivo = list(reader)
            lista_por_arquivo.pop(0)
            data +=  lista_por_arquivo
    data = []

    open_file('parsed_discurso_2018_dit_concat.csv',data)

    body = []
    for d in data:
        body.append(d[3])

    stopwords = nltk.corpus.stopwords.words("portuguese")

    regex = "[a-zA-ZçÇãÃõÕáÁéÉíÍóÓúÚâÂêÊîÎôÔûÛàÀ]+"

    documents_without_stopwords = [[stemmer.stem(remover_combinantes(w.lower())) for w in word_tokenize(text) if w.lower() not in stopwords and stemmer.stem(remover_combinantes(w.lower())) not in estadosBrasileirosStem] 
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

lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=20)

lsi.save(BASEDIR+"/model_discursos.lsi") 

index = similarities.Similarity(BASEDIR+"/index",lsi[corpus],num_features=len(dictionary),num_best=len(data))

vec_lsi = lsi[corpus_tfidf[0]]
# topicos = [['lula','violência','mulher','petrobrás'],
# ['lula','golpe','petrobrás'],
# ['lula','educação'],
# ['lula','educação'],
# ['mulher','lula','violência','petrobrás'],
# ['consumidor','pesca'],
# ['pesca','rodovia'],
# ['feliciano','petrobrás','agricultura'],
# ['igreja','israel'],
# ['bolsonaro','policia','deus'],
# ['lula'],
# ['igreja','lula','eletrobrás'],
# ['igreja','pesca'],
# ['mulher','caminhoneiro','consumidor','agricultura'],
# ['igreja','petrobrás','consumidor'],
# ['esporte','turismo','pesca'],
# ['turismo','imigração','segurança'],
# ['turismo','pesca','imigração','esporte','segurança'],
# ['consumidor','mulher','pesca','segurança'],
# ['turismo','pesca','agricultura']
# ]

sims = index[vec_lsi]

for i in range(len(data)):
    vec_lsi = lsi[corpus_tfidf[i]]
    v = sorted(vec_lsi,key= lambda x: x[1],inverse=True)

