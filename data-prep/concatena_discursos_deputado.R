library(dplyr)
library(stringr)

discursos_deputados <- read.csv2('/home/tarciso/workspace/me-diz-quem-tu-es/DadosDeDiscurso/Dados/parsed_discurso_2018_dit.csv') %>%
  mutate(deputado = trimws(gsub("\\(.*", "", deputado)))

discursos_deputados_qtd <- discursos_deputados %>%
  na.omit() %>%
  group_by(deputado) %>%
  summarise(num_discursos = n(),
	    partido = last(partido),
	    uf = last(uf))

selected_deputados <- discursos_deputados_qtd %>%
  filter(num_discursos >= 3)

discursos_deputados_selecionados <- discursos_deputados %>%
  select(-timestamp, -partido, -uf) %>%
  merge(selected_deputados) %>%
  group_by(deputado, partido, uf) %>%
  summarise(discurso_total = paste(Discurso, collapse=' '))

str(discursos_deputados_selecionados)

write.csv2(discursos_deputados_selecionados,'/home/tarciso/workspace/me-diz-quem-tu-es/DadosDeDiscurso/Dados/discursos_concatenados_2018.csv', row.names=F)
