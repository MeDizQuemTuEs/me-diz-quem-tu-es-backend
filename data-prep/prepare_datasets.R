library(dplyr)
library(stringr)

data_folder <- './Dados'
anos <-c(2016:2018)

output_path_discursos_sep = paste(data_folder,'discursos_sep.csv',sep='/')
output_path_discursos_concat = paste(data_folder,'discursos_concat.csv',sep='/')

discursos_sep = data.frame()

for(ano in anos) {
  input_path <- paste(data_folder,paste0('parsed_discurso_', ano, '_dit.csv'),sep='/')  
  discursos_sep <- read.csv2(input_path) %>%
    mutate(deputado = trimws(gsub("\\(.*", "", deputado))) %>%
    na.omit() %>%
    rbind(discursos_sep,.)
}

write.csv2(discursos_sep,output_path_discursos_sep, row.names=F)

discursos_deputados_qtd <- discursos_sep %>%
  group_by(deputado) %>%
  arrange(timestamp) %>%
  summarise(num_discursos = n(),
            partido = last(partido),
            uf = last(uf))

selected_deputados <- discursos_deputados_qtd %>%
  filter(num_discursos >= 10)

discursos_deputados_selecionados_concat <- discursos_sep %>%
  select(-timestamp, -partido, -uf) %>%
  merge(selected_deputados) %>%
  group_by(deputado, partido, uf) %>%
  summarise(discurso_total = paste(Discurso, collapse=' '))

write.csv2(discursos_deputados_selecionados_concat,output_path_discursos_concat, row.names=F)