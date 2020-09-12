# Project Charter

## Entendimento de negócio

Forex é um tipo de investimento baseado na variação do câmbio entre várias moedas e é um mercado muito volátil e de alto risco.

A construção da base de dados será baseada em uma API pública que irá fornecer dados históricos de cotação do Forex.

Deseja-se utilizar a informação desse histórico para prever a cotação no período seguinte (30 minutos) a fim fazer investimentos dentro desse tempo.


## Escopo

O problema pode ser abordado como forcast, já que envolve a previsão de uma variável contínua (o valor da cotação) ao longo do tempo. Como as bases já estão avaliadas previamente, trata-se de um problema para algoritmos de treinamento supervisionado.

* **Problema**: forecast
* **Algoritmo**: treinamento supervisionado
* **Base de dados**: API pública com dados históricos (https://fcsapi.com/)
* **Variável alvo**: valor da cotação

## Métricas
* Objetivo qualitativo: prever o valor da cotação.
* Figura de mérito: MAPE.
* Benchmarking: melhor que o aleatório de 50%.

## Planejamento
* Sprint 1: entendimento de negócio e preparação dos dados.
* Sprint 2: Análise de dados e construção de features.
* Sprint 3: Modelagem dos classificadores e avaliação dos resultados
* Sprint 4: Relatório dos resultados do modelo

## Arquitetura

* Dados:
  * Os dados são entregues através de API pública (https://fcsapi.com/)
  * Relatório de dados disponível [aqui](./DataReport.md "Relatório de dados")

* Modelos:
  * Forecast para estimar o valor da cotação no próximo período.
  * Será utilizado um modelo de forecast.
  * Os hiper-parâmetros dos modelos serão ajustados segundo uma busca exaustiva em grid-search.
  * A base de dados será dividida em treino (80%) e teste (20%).
  * Os modelos serão avaliados considerando o conjunto de teste.
  * Os modelos e as análises sobre os dados podem ser estudadas [aqui](ModelReport.md "Relatório de modelagem")
  
* Entregáveis:
  * Apresentação com os resultados mais relevantes.
  * Base de dados de teste com a estimativa do valor da cotação.

## Detalhes da Solução

Haverá um serviço disponível para fazer a previsão da cotação nos próximos 30 minutos. Toda vez que o serviço executar ele seguirá os seguintes passos:

* Atualizar a base de dados local: Parte dos dados (histórico) para treinamento já estará armazenada localmente. O serviço irá verificar a data do último evento e recuperará os eventos desde essa data até o momento da execução. Isso manterá a base histórica atualizada e permitirá o treinamento com dados atualizados.

* Treinar o modelo: Após atualizar a base histórica, o serviço fará o treinamento do modelo com dados atuais.

* Previsão do próximo período: Com o modelo treinado, os próximos 30 minutos serão previstos.

* Armazenamento da previsão: Os dados da previsão será persistidos para acompanhamento da eficiência e melhoria do processo.

Os dados históricos, as execuções e as previsões poderão ser consultados em uma aplicação Web feita para esse fim. Os dados das previsões poderão ser comparados com os dados históricos para avaliação do desempenho.
