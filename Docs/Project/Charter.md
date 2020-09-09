# Project Charter

## Entendimento de negócio

O objetivo é criar uma aplicação onde os usuários possam identificar a raça de seu cachorro enviando uma foto.


## Escopo

O problema de calassificação pode ser abordado como um problema de classificação. Como as bases já estão avaliadas previamente, trata-se de um problema para algoritmos de treinamento supervisionado. A quantidade de possíveis valores para as classes indica que é um problema de classificação não binária.

* **Problema**: classificação
* **Algoritmo**: treinamento supervisionado
* **Base de dados**: APi com base de imagens
* **Variável alvo**: Raça do cachorro

## Métricas
* Objetivo qualitativo: estimar a raça do cachorro.
* Figura de mérito: acurácia.
* Benchmarking: melhor que o aleatório de 50%.
* Métrica deve ser medida sobre um conjunto de teste de 20% dos dados para cada classe.


## Planejamento
* Sprint 1: entendimento de negócio e preparação dos dados.
* Sprint 2: Análise de dados e construção de features.
* Sprint 3: Modelagem dos classificadores e avaliação dos resultados
* Sprint 4: Relatório dos resultados do modelo

## Arquitetura

* Dados:
  * Os dados são entregues através de 1 arquivo CSV
  * Relatório de dados disponível [aqui](../DataReport/Report.md "Relatório de dados")

* Modelos:
  * Classificador para estimar a probabilidade de cada raça.
  * Será utilizado o modelo não-linear: RandomForest.
  * Os hiper-parâmetros dos modelos serão ajustados segundo uma busca exaustiva em grid-search.
  * A base de dados será dividida em treino (80%) e teste (20%), mantendo a proporção de classes nos dois conjuntos de dados.
  * Os modelos serão avaliados considerando o conjunto de teste.
  * Os modelos e as análises sobre os dados podem ser estudadas [aqui](../Model/Report.md "Relatório de modelagem")
  
  
* Entregáveis:
  * Apresentação com os resultados mais relevantes.
  * Base de dados de teste com a probabilidade de sentimento positivo dos comentários, em arquivo Excel.


