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

BASEDIR = os.getcwd()

dados_dict = {}
for i in range(len(data)):
    try:
        if(int(data[i][0]) > 0):
            if data[i][1] in dados_dict:
                dados_dict[data[i][1]].append([data[i][4],data[i][5]])
            else:
                dados_dict[data[i][1]] = []
                dados_dict[data[i][1]].append([data[i][4],data[i][5]])
    except:
        pass


for dic in dados_dict:
    with open("discursos/"+dic+".json", 'w',encoding='utf8') as outfile:
        json.dump({dic: dados_dict[dic]},outfile, ensure_ascii=False)
