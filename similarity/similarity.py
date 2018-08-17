import gensim, nltk, re, json, os
from gensim import corpora,similarities, models
from nltk.tokenize import word_tokenize
from datetime import date,datetime
import csv 
import base64
csv.field_size_limit(100000000)


data = []

with open('parsed_discurso_2018_dit.csv', 'r') as f:
    reader = csv.reader(f,delimiter=';')
    data = list(reader)

discurssos = []
# for d in data:
#     discurssos.append(d[0].split(";"))

body = []

for i in range(len(discurssos)):
        try:
            if(len(discurssos[i][5]) > 15):
                body.append(str(base64.b64decode(discurssos[i][5])))
        except:
            pass

BASEDIR = os.getcwd()
if (os.path.exists(BASEDIR+"/discurssos_dict.dict") and (os.path.exists(BASEDIR+"/discurssos_corpus.dict") & (os.path.exists(BASEDIR+"/model_discurssos.dict") ):
   dictionary = corpora.Dictionary.load(BASEDIR+"/discurssos_dict.dict")
   corpus = corpora.MmCorpus(BASEDIR+"/discurssos_corpus.mm")
   lsi = models.LsiModel.load(BASEDIR+"/model_discurssos.lsi")
else:
    stopwords = nltk.corpus.stopwords.words("portuguese")

    regex = "[a-zA-ZçÇãÃõÕáÁéÉíÍóÓúÚâÂêÊîÎôÔûÛàÀ]+"

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

    dictionary.save(BASEDIR+"/discurssos_dict.dict")

    corpus = [dictionary.doc2bow(document) for document in documents]

    corpora.MmCorpus.serialize(BASEDIR+"/discurssos_corpus.mm", corpus)

    tf_idf = models.TfidfModel(corpus)

    corpus_tfidf = tf_idf[corpus]

    lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary)

    lsi.save(BASEDIR+"/model_discurssos.lsi") 

vec_lsi = lsi[corpus_tfidf[0]] # convert the query to LSI space 300/100/0

# index = similarities.MatrixSimilarity(corpus= lsi[corpus],num_best=5)
index = similarities.Similarity(BASEDIR+"/index",lsi[corpus],num_features=len(dictionary),num_best=5)
sims = index[vec_lsi]

