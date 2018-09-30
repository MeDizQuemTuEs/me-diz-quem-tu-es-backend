library(dplyr, quietly = TRUE, verbose = FALSE)
pasta_base <- "C:/Users/jeffe/workspace/HackFest-2018"
setwd(pasta_base)
source('http://www.sthda.com/upload/rquery_wordcloud.r')
library('tm')
library('SnowballC')
library('wordcloud')
library('RColorBrewer')
library('stringr')

base_de_dados <- read.csv2("Dados/discursos_concat.csv", fileEncoding="UTF-8")

nome_dos_deputados <- read.csv2("Dados/deputados.csv", fileEncoding="UTF-8") %>%
  select(nome) %>% distinct()

generate_wordcloud_graph <- function(base, nome_dep) {
  nome_stop_words <- nome_dep
  
  disc_dep_ind <- base
  
  disc_dep_ind$deputado <- as.character(disc_dep_ind$deputado)
  
  disc_dep_ind <- disc_dep_ind %>% filter(deputado == nome_dep)
  
  discurso <- VCorpus(VectorSource(disc_dep_ind$discurso_total))
  
  # Converter o corpus em um documento de texto simples
  discurso <- tm_map(discurso, PlainTextDocument)
  
  # Remover numeros
  discurso <- tm_map(discurso, removeNumbers)
  
  # Remover Pontuacao
  discurso <- tm_map(discurso, removePunctuation)
  
  #Colocar todas as palavras em caixa baixa
  discurso <- tm_map(discurso, content_transformer(tolower))
  
  #
  discurso <- tm_map(discurso, removeWords, stopwords("pt"))
  
  
  stop_word <- c('acre','jos','mineiro', 'mineiros','angra','alagoas','amapá','amazonas',
                   'bahia', 'ceará','distrito','federal','espírito','espiríto','goiás','maranhão',
                   'mato grosso', 'minas', 'minas gerais', 'pará' , 'paraíba' , 'paraná', 'pernambuco',
                   'piauí', 'rio de janeiro' ,' rio grande do norte', 'rio grande do sul',
                   'rondônia', 'roraima', 'santa','catarina', 'santa catarina', 'são paulo' ,'sergipe',
                 'tocantins','hugs','sra','soray','cnec','sessão','lucia', 'borges','medalha','janeiro',
                 'convido','bilhões','taquigrafia','creuz','leal','alternativa','piauhylin',
                 'silva','creuza','benedet', 'martell','zeraik','benedet','dalva','medeira',
                 'pollyana','colm','borge','frag','gonzaga','ronaldo', 'celina','dalva','colm', 'srs',
                 'ser', 'arquivo', 'sras', 'obrigado', 'aqui', 'todos', 'vem', 'toda', 'presidente',
                 'deputado')
  
  
  discurso <- tm_map(discurso, removeWords, stop_word)
  
  res<-rquery.wordcloud(discurso, type ="text", lang = "portuguese",
                        min.freq = 10,  max.words = 100, excludeWords = stop_word,
                        colorPalette = 'Dark2')
}

setwd(paste0(pasta_base, '/deputados_grafico_wordcloud'))
for (nome in nome_dos_deputados$nome) {
  nome_doc <- paste0(nome, '.png')
  png(nome_doc, width=360, height=360)
  generate_wordcloud_graph(base = base_de_dados, nome_dep = nome)
  dev.off()
}
setwd(pasta_base)

