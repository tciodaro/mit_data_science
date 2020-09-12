
# Relatório de Dados

Esse relatório das bases de dados do projeto.


## Bases de dados

A base de dados (origem dos dados) será a API pública https://fcsapi.com/document/forex-api.

Essa API oferece o serviço de consulta de histórico do Forex com intervalo mínimo de 1 minuto, que é o que iremos utilizar.

Os dados oferecidos pela API são os dados do candle: 
* Open: Valor de abertura
* Low: Valor mínimo do candle
* Hight: Pico do candle
* Close: Valor de fechamento
* Time: Data e hora da cotação

Os dados são coletados em [data_collect.ipynb](../code/data_collect.ipynb) e são tratados em [data_prep.ipynb](../code/data_prep.ipynb).

## Análise dos Dados

Durante a análise dos dados foi verificado que não há dados faltantes e que os campos open, low e hight tem uma correlação de 100% com a variável alvo. Por esse motivo essas variáveis foram descartadas e em seu lugar foram utilizadas novas features a partir da própria variável alvo regredidas em intervalos de tempo para tentar capturar relações entre esses intervalos e o valor futuro.
