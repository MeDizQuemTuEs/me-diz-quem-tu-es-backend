library(networkD3, quietly = TRUE, verbose = FALSE) # Cria grafico com grafo
library(magrittr) # exporta para uma pagina html
library(dplyr, quietly = TRUE, verbose = FALSE)
pasta_base <- "C:/Users/jeffe/workspace/HackFest-2018"
setwd(pasta_base)

base_de_dados <- read.csv2("Dados/deputados.csv", fileEncoding="UTF-8") 
base_rename <- dplyr::rename(base_de_dados, similaridade = pontuacao)
base_rename$similaridade <- as.numeric(as.character(base_rename$similaridade))

generate_similarity_graph <- function(dep_id, base) {

mais_similares <-  base %>% 
  filter(id == dep_id) %>%
  top_n(6)

nodes_df <- mais_similares %>%
  select(nomeComparado,partidoComparado) %>%
  mutate(nomeComparado = paste(nomeComparado,'-',partidoComparado), 
    node_size = c(1200,rep(600,5)))

links_df <- mais_similares %>%
  select(similaridade) %>%
  mutate(src=rep(0,nrow(nodes_df)),
        target=0:(nrow(nodes_df)-1))

nome <- base %>% filter(id == dep_id) %>% select(nome) %>% distinct()
setwd(paste0(pasta_base, "/deputados_grafico"))

nome <- gsub(" ", "_", nome$nome)

arq_graf <- paste0(nome, '.html')

forceNetwork(Links = links_df, Nodes = nodes_df,
             Source = "src", 
             Target = "target",
             Value = "similaridade", 
             NodeID = "nomeComparado",
             Group = "partidoComparado",
             linkColour = "lightgrey",
             Nodesize = "node_size",
             opacity = 1, 
             fontSize = 20,
             colourScale = JS("d3.scaleOrdinal(d3.schemeCategory10);"),
             charge = -1300,
             linkDistance = 250, 
             fontFamily = "serif",
             opacityNoHover = 0.3,
             zoom = TRUE) %>%
  saveNetwork(file = arq_graf)
}


for (i in 0:476) {
  
  generate_similarity_graph(base = base_rename, dep_id = i)
  
}
setwd(pasta_base)





