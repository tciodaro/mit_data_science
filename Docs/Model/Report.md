# Relatório de Modelagem

Documento para registrar as análises e a modelagem desenvolvida.


## Análise de Dados

Os dados são obtidos a partir de busca de imagens da DOG API. Cada foto é transformada em uma lista de pixels e um último campo com a raça do cachorro. Devido à forma como os dados são gerados estes já estão normalizados e não nulos.


### Modelo

O modelo utilizado foi o Random Forest. Utilizado também o PCA (Principal Component Analisys) para melhoria dos resultados.

## Próximos passos

Após a análise preliminar, devemos seguir com o treinamento dos modelos de classificação, utilizando validação cruzada como forma de estimar os hiper-parâmetros do modelo que conseguem a melhor generalização possível.

