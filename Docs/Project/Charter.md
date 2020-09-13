# Project Charter

## Objetivo
O projeto foi concebido para estimar, baseado no texto descritivo sobre a manutenção do equipamento de rede elétrica, quem seria o responsável pela execução do serviço

## Entendimento de negócio
A rede elétrica é composta por diversos equipamentos, como linhas de transmissão, disjuntores, transformadores, chaves, conector e outros, que em harmonia, permitem que a energia seja gerada e transportada até as nossas casas. Estes equipamentos são dispositivos mecânicos que tem uma vida finita e necessitam de manutenção periódica. Devido a criticidade, especificidade e quantidade, os equipamentos podem ter a sua manutenção supervisionado pela empresa que os opera ou pelo próprio proprietário, e esta decisão é atualmente realizada sem intervenção computacional. 


## Escopo

Os dados a serem analisados para treino e testes são os textos de manutenção já classificados quanto a responsabilidade do período de jan-2019 a mai-2020, em torno de 22.700 registros. 

A abordagem a ser aplicada para a predição será a mesma para problemas de analise de sentimentos, ou seja, problemas de classificação binária com a utilização de algoritmos de treinamento supervisionado para esta estimação.

* **Atributos Preditores**: Descrição da manutenção do equipamento
* **Atributo Alvo**: Tipo de Supervisão (OPER – Operador ou PROP – Proprietário)
* **Base de Treino**:  78% dos dados originais
* **Base de Teste**:   22% dos dados originais
* **Arquitetura:**Uso de Django para criação de API.REST e Base de dados SQLLite

## Resumo Descritivo
* **Problema**: classificação binária
* **Algoritmo**: treinamento supervisionado
* **Base de dados**: arquivo csv com comentários de texto livre
* **Variável alvo**: Sentimento positivo ou negativo

## Métricas
* Objetivo qualitativo: estimar a supervisão dos equipamentos
* Figura de mérito: f1-score.
* Benchmarking: melhor que o aleatório de 50%.
* Métrica deve ser medida sobre um conjunto de teste de 22% dos dados para cada classe.


## Planejamento
* Sprint 1: entendimento de negócio e preparação dos dados.
* Sprint 2: Análise de dados e construção de features.
* Sprint 3: Modelagem dos classificadores e avaliação dos resultados
* Sprint 4: Relatório dos resultados do modelo


## Arquitetura

* Dados:
  * Os dados são entregues através de 1 arquivo CSV
  * Relatório de dados disponível (../Project/Results.pdf "Relatório de dados")

* Modelos:
  * Classificador binário para estimar a probabilidade do comentário
  * Será utilizado um modelo linear de Regressão Logística.
  * Serão utilizados três modelos não-lineares: RandomForest, SVM e o kNN.
  * Os hiper-parâmetros dos modelos serão ajustados segundo uma busca exaustiva em grid-search.
  * A base de dados será dividida em treino (78%) e teste (22%), mantendo a proporção de classes nos dois conjuntos de dados.
  * Os modelos serão avaliados considerando o conjunto de teste.
  * Os modelos e as análises sobre os dados podem ser estudadas 
  
  
* Entregáveis:
  * Apresentação com os resultados mais relevantes.
  * Base de dados de teste com a probabilidade de sentimento positivo dos comentários, em arquivo Excel.
  * [aqui](../Model/ReportModelo.xlsx "Graficos")


