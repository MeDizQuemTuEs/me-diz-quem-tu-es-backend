import requests
import csv
import io

NUMERO_MAX_PAG = 35

## retorna a url com a pagina informada
def __get_url_pag(pagina):
	url_1 = "https://dadosabertos.camara.leg.br/api/v2/deputados?pagina="
	url_2 = "&ordem=ASC&ordenarPor=nome"
	return (url_1 + str(pagina) + url_2)	

## grava em arquivo csv a lista de deputados passados
def __gravar_csv(deputados):
	with open("deputados.csv", 'w') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(["nome", "siglaPartido", "siglaUf", "urlFoto"])
		for deputado in deputados:
			spamwriter.writerow([deputado["nome"], deputado["siglaPartido"], deputado["siglaUf"], deputado["urlFoto"]])

list_deputados = []

for i in range(1, NUMERO_MAX_PAG+1):
	r = requests.get(__get_url_pag(i)).json()
	result = r["dados"]
	for i in range(len(result)):
		list_deputados.append(result[i])

__gravar_csv(list_deputados)
