install.packages("read.dbc")
library("read.dbc")


# url <- "ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/PRELIM/DORES/DOAC23.dbc"
# download.file(url, destfile = "DOAC23.dbc", mode = "wb")
# dopr <- read.dbc("DOAC23.dbc")
# write.csv(dopr, file = "dados/DOAC23.csv", row.names=FALSE)
# ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/PRELIM/DORES/DOSP2022.dbc

estados <- c("AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO")
anos <- as.character(1979:2023)


# Loop para substituir {Estado} e {Ano} e realizar as operações
for (estado in estados) {
  for (ano in anos) {
    # print(ano)
    tryCatch({
      # Substituir {Estado} e {Ano} na URL
      url <- sprintf("ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DORES/DO%s%s.dbc", estado, ano)
      
      # Nome do arquivo para download
      arquivo <- sprintf("DO%s%s.dbc", estado, ano)
      
      # Download do arquivo
      download.file(url, destfile = arquivo, mode = "wb")
      
      # Ler o arquivo DBC
      dopr <- read.dbc(arquivo)
      
      # Nome do arquivo CSV de saída
      csv_saida <- sprintf("datasus-analysis-main/dados/DO%s%s.csv", estado, ano)
      
      # Escrever o arquivo CSV
      write.csv(dopr, file = csv_saida, row.names = FALSE)
      
      # Mensagem de conclusão para cada iteração
      cat(sprintf("Arquivos para %s - %s criados.\n", estado, ano))
    }, error = function(e) {
      cat(sprintf("Erro ao processar %s - %s: %s\n", estado, ano, e$message))
      # Pode adicionar código adicional aqui para lidar com o erro, se necessário
    })
  }
}