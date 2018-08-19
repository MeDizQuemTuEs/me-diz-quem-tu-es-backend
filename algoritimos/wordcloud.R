library(wordcloud)
library(tm)

pedro_discursos <- read.csv2('./Dados/pedro_cl.csv', header = F)

# Da biblioteca tm. Corpus para o treinamento. Utilizando apenas os ingredientes.
ingredientes <- VCorpus(VectorSource(pedro_discursos$V1))

# Converter o corpus em um documento de texto simples
ingredientes <- tm_map(ingredientes, PlainTextDocument)

# Remover numeros
ingredientes <- tm_map(ingredientes, removeNumbers)

# Remover Pontuacao
ingredientes <- tm_map(ingredientes, removePunctuation)

#Colocar todas as palavras em caixa baixa
ingredientes <- tm_map(ingredientes, content_transformer(tolower))

# Remover palavras desinterecantes com (or, and, of, the)
# removeWords(ingredientes, words = c(stopwords("en"), stopwords("pt"))) ou tm_map(ingredientes, removeWords, stopwords('pt'))
ingredientes <- tm_map(ingredientes, removeWords, stopwords("pt"))

# Para evitar palavras semelhantes uma solução é pegar e unir as palavras com mesmo radical
# Verificar palavras semelhantes (mesmo radical)
#ingredientes <- tm_map(ingredientes, stemDocument)

#Remover palavras de (materiais) e de tamanho como: (pequeno medio e grande)
#ingredientes <- tm_map(ingredientes, removeWords, c("active", "adobo", "aged", "ahi", "american", "angel", "can", "packag"))

wordcloud::wordcloud(ingredientes, max.words = 50)
