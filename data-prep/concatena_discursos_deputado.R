library(dplyr)
library(stringr)

data_folder <- './Dados'
ano <- 2018

input_path <- paste(data_folder,paste0('parsed_discurso_', ano, '_dit.csv'),sep='/')

discursos_deputados <- read.csv2(input_path) %>%
  mutate(deputado = trimws(gsub("\\(.*", "", deputado)))

discursos_deputados_qtd <- discursos_deputados %>%
  na.omit() %>%
  group_by(deputado) %>%
  arrange(timestamp) %>%
  summarise(num_discursos = n(),
	    partido = last(partido),
	    uf = last(uf))

selected_deputados <- discursos_deputados_qtd %>%
  filter(num_discursos >= 3)

discursos_deputados_selecionados_sep <- discursos_deputados %>%
  select(-timestamp, -partido, -uf) %>%
  merge(selected_deputados)

discursos_deputados_selecionados_concat <- discursos_deputados_selecionados_sep %>%
  group_by(deputado, partido, uf) %>%
  summarise(discurso_total = paste(Discurso, collapse=' '))

str(discursos_deputados_selecionados_sep)

str(discursos_deputados_selecionados_concat)

output_path_discursos_sep = paste(gsub('.csv','_sep.csv',input_path))

output_path_discursos_concat = paste(gsub('.csv','_concat.csv',input_path))

write.csv2(discursos_deputados_selecionados_sep,output_path_discursos_sep, row.names=F)
write.csv2(discursos_deputados_selecionados_concat,output_path_discursos_concat, row.names=F)
