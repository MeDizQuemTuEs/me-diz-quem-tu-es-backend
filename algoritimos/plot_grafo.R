library(networkD3, quietly = TRUE, verbose = FALSE) # Cria grafico com grafo
library(magrittr) # exporta para uma pagina html
library(dplyr, quietly = TRUE, verbose = FALSE)

setwd("C:/Users/jeffe/workspace/HackFest-2018")

base_de_dados <- read.csv2("Dados/deputados.csv", fileEncoding="UTF-8") 
base_de_dados_clusters <- read.csv("Dados/clusters.csv", fileEncoding="UTF-8") 
base_de_dados_a <- merge(base_de_dados, base_de_dados_clusters, by = "id")
base_rename <- dplyr::rename(base_de_dados_a, similaridade = pontuacao)
base_rename$similaridade <- as.numeric(as.character(base_rename$similaridade))

mais_similares <-  base_rename %>% filter(id < idComparado)

mais_similares <- mais_similares %>% group_by(nome) %>% mutate(peso = sum(similaridade))


gropo_e_id <- tibble(name=paste0(mais_similares$nome, " - ", mais_similares$partido), 
                     group=mais_similares$partido, similaridade_peso=mais_similares$peso)  %>% 
                      distinct()

links <- tibble(source=mais_similares$id, target=mais_similares$idComparado, 
                value=mais_similares$similaridade) %>% 
  filter(value > 0.6)

forceNetwork(Links = links, Nodes = gropo_e_id,
             Source = "source", 
             Target = "target",
             Value = "value", 
             NodeID = "name",
             Group = "group",
             linkColour = "lightgrey",
             Nodesize = "similaridade_peso",
             opacity = 1, 
             fontSize = 12,
             colourScale = JS("d3.scaleOrdinal(d3.schemeCategory10);"),
             charge = -15,
             linkDistance = 50, 
             opacityNoHover = 0.3,
             zoom = TRUE) %>%
            saveNetwork(file = 'grafo.html')