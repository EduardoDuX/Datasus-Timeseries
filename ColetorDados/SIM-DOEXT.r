install.packages("read.dbc")
library("read.dbc")


anos <- as.character(1979:2023)

# Loop para substituir {Ano} e realizar as operações
for (ano in anos) {
    tryCatch({
        # Substituir} e {Ano} na URL
        ano <- substring(ano, 3, 4)
        # 'ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID9/DOFET/DOEXT79.DBC'
        url <- sprintf("ftp://ftp.datasus.gov.br/dissemin/publicos/SIM/CID10/DOFET/DOEXT%s.dbc", ano)
        
        # Nome do arquivo para download
        arquivo <- sprintf("dados/DOEXT%s.dbc", ano)
        
        # Download do arquivo
        download.file(url, destfile = arquivo, mode = "wb")
        
        # Ler o arquivo DBC
        dopr <- read.dbc(arquivo)
        
        # Nome do arquivo CSV de saída
        csv_saida <- sprintf("dados/DOEXT%s.csv", ano)
        
        # Escrever o arquivo CSV
        write.csv(dopr, file = csv_saida, row.names = FALSE)
        
        # Mensagem de conclusão para cada iteração
        cat(sprintf("Arquivos para %s criados.\n", ano))
    }, error = function(e) {
        cat(sprintf("Erro ao processar %s: %s\n", ano, e$message))
        # Pode adicionar código adicional aqui para lidar com o erro, se necessário
    })
}