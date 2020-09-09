
# Relatório de Dados

Esse relatório das bases de dados do projeto.


## Bases de dados


| Nome Dataset | Origem   | Destino  | Script |
| ---:| ---: | ---: | ---: | -----: |
| Fotos de raças de cachorro | Dogs API | Arquivo parquet | [data_prep.ipynb](../../Code/DataPrep/data_prep.ipynb) | 


* Base de Fotos

Possui as fotos com os pixels linearizados de forma que cada coluna rpresenta um pixel.
Atualmente as fotos são dimensionalizadas no tamanho 64x64.

A última columa é a raça real do cachorro.
Devido a natureza da geração dos dados não há dados nulos.





