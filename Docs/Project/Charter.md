# Project Charter

## Entendimento de negócio

PJM Interconnection LLC (PJM) é uma organização de transmissão regional (RTO) nos Estados Unidos. É parte da rede de interconexão oriental que opera um sistema de transmissão elétrica que atende a totalidade ou parte de Delaware, Illinois, Indiana, Kentucky, Maryland, Michigan, Nova Jersey, Carolina do Norte, Ohio, Pensilvânia, Tennessee, Virgínia, Virgínia Ocidental e o distrito de Columbia.
Os dados de consumo de energia por hora vêm do site da PJM e estão em megawatts (MW).
A PJM é um dos maiores mercados atacadistas de eletricidade do mundo, abrangendo mais de 1.000 empresas, 65 milhões de clientes e entregou 807 terawatts-hora de eletricidade em 2018.
No setor de eletricidade, ser capaz de prever o uso de eletricidade no futuro é essencial e uma parte central dos negócios de qualquer varejista de eletricidade. O uso de eletricidade pelos clientes de um varejista de eletricidade é geralmente conhecido como 'carga' do varejista e a curva de uso é conhecida como 'curva de carga'.
Ser capaz de prever a carga com precisão é importante por uma série de razões:
Preveja a carga base futura - os varejistas de eletricidade precisam ser capazes de estimar com antecedência quanta eletricidade eles precisam comprar da rede. Suavizar o preço - se a carga for conhecida como antecipada, os varejistas de eletricidade podem se proteger contra o preço para garantir que não sejam pegos quando o preço disparar 3 meses no futuro.
Resumindo, o problema de negócios é:
Dado o consumo de energia histórico, qual é o consumo de energia esperado para os próximos 5 dias?

## Escopo

A previsão da demanda de energia pode ser abordado como um problema de forecasting. A previsão de dados de série temporal é diferente de outras formas de problemas de aprendizado de máquina devido a um motivo principal - os dados de série temporal geralmente estão correlacionados com o passado. Ou seja, o valor de hoje é influenciado, por exemplo, pelo valor de ontem, pelo valor da semana passada, etc. Isso é conhecido como 'autocorrelação' (ou seja, correlação com 'self').


* **Problema**: forecasting
* **Algoritmo**: treinamento supervisionado
* **Base de dados**: API json
* **Variável alvo**: Consumo em Megawatts

## Métricas
* Objetivo qualitativo: estimar o consumo de energia para os próximos 5 dias .
* Figura de mérito: MAPE.
* Benchmarking: MAPE no máximo em 10%, considerando um período total de 24 horas.
* Métrica deve ser medida comparando os 5 dias que foram previstos com os dados reais a serem coletados. 


## Planejamento
* Sprint 1: Entendimento de negócio e preparação dos dados.
* Sprint 2: Análise de dados e construção de features.
* Sprint 3: Modelagem dos classificadores e avaliação dos resultados
* Sprint 4: Relatório dos resultados do modelo
* Sprint 5: Configuração de servidor web Django para implantação do modelo e disponibilização de serviços de atualização de dados, treinamento do modelo, previsão de demanda e avaliação da previsão da demanda. 
* Sprint 6: Configuração de ferramenta de visualização Dash para geração dos gráficos

## Arquitetura

* Dados:
  * Os dados são entregues através de API Json
  * Relatório de dados disponível [aqui](../DataReport/Report.md "Relatório de dados")

* Modelos:
  * Modelo de forecasting baseado em análise regressiva.  
  * Serão utilizados quatro modelos: Prophet, Arima, LASSO e Holtwinters  
  * A base de dados será dividida em treino (80%) e teste (20%), mantendo a proporção de classes nos dois conjuntos de dados.
  * Os modelos serão avaliados considerando o conjunto de teste.
  * Os modelos e as análises sobre os dados podem ser estudadas [aqui](../Model/Report.md "Relatório de modelagem")
  
  
* Entregáveis:
  * Apresentação com os resultados mais relevantes.
  * Base de dados de teste com as previsões de consumo e dados históricos. 
  * Notebooks com códigos de limpeza dos dados, de análise dos dados e de construção dos modelos.
  * Página Web, baseado no servidor Django, com acesso a recursos “Rest” específicos para atualização de dados, treinamento do modelo, previsão de demanda de energia e avaliação da exatidão da previsão. 
  * Página Web com gráfico (Dash) que permitirá avaliação contínua da qualidade de previsão, sempre baseada nos dados mais recentes. 
  * Notebooks com códigos de limpeza dos dados, de análise dos dados e de construção dos modelos.
  * Base de dados Sqlite3 com informações históricas e previsões de demanda de energia. 
  
  
  


