library(dplyr)
library(reshape2) 
library(ggplot2)

discursos_dist <- read.csv2('./Dados/deputados.csv') %>%
  mutate(pontuacao = as.numeric(as.character(pontuacao)))

discursos_dist <- discursos_dist %>%
  mutate(dist = 1 - pontuacao)

discursos_dist_mat <- as.dist(acast(discursos_dist, id~idComparado, value.var = 'dist'), diag=TRUE)

clusters <- hclust(as.dist(discursos_dist_mat, diag=TRUE))

clusters_df <- data.frame(id = row.names(data.frame(cutree(clusters, k=2))),
                          k2 = cutree(clusters, k=2), 
                          k3 = cutree(clusters, k=3), 
                          k4 = cutree(clusters, k=4),
                          k5 = cutree(clusters, k=5))

write.csv(clusters_df, './Dados/clusters.csv', row.names = F)

plot(clusters)

ggplot(discursos_dist, aes(Petal.Length, Petal.Width, color = iris$Species)) + 
  geom_point(alpha = 0.4, size = 3.5) + geom_point(col = clusterCut) + 
  scale_color_manual(values = c('black', 'red', 'green'))

plot(clusters)

df <- data.frame(point1 = c(1,2),
                 point2 = c(2,1),
                 dist = c(0.4,0.4))

dist(df)
dist_mat <- acast(df, point1~point2)
clusters <- hclust(as.dist(dist_mat, diag=TRUE))

plot(clusters)

mydata=read.table(textConnection("point1    point2    distance 
1              1            0 
1              2            4 
2              2            0 
2              1            4"),header=TRUE) 

iris[, 3:4]
