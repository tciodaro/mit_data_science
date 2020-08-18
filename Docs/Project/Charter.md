# Project Charter

## Entendimento de negócio

Retail Co. é uma empresa de lojas de departamentos, com 45 lojas localizadas em diferentes localidades. Cada loja possui uma quantidade de departamentos, onde produtos de diversos tipos são vendidos. Frequentemente, a empresa investe em propagandas e promoções (Markdown), que geralmente são feitas antes de feriados importantes, como super bowl, dia do trabalho...



## Escopo

A empresa gostaria de investir numa solução baseada em dados para auxiliar os consultores da empresa em suas decisões de planejamento de vendas e logística. Para isso, a empresa fez uma coleta de histórico semanal de suas vendas, em conjunto com um grupo de variáveis que são consideradas interessantes para o entendimento do volume de vendas.

* A solução deve observar o histórico de dados e fazer a previsão das próximas semanas.
* Os dados serão coletadas através de arquivos CSV de um servidor FTP.
* O resultado da previsão será exportado como arquivo CSV.
* O resultado pode ser consumido em relatórios estáticos.

## Pessoal
* Quem está no projeto:
	* Consultoria:
		* Project lead (Thiago)
		* PO (Thiago)
		* Data scientist(s) (Oliveira, Machado)
		* Account manager (Oliveira)
	* Retail Co:
		* Data administrator
		* Business contact

## Métricas
* Objetivo qualitativo: otimizar o planejamento da planta de produção.
* Figura de mérito: erro absoluto percentual médio (MAPE)
* Benchmarking: processo atual trabalha com um MAPE de aproximadamente 50%.
* Métrica deve ser medida sobre todo o histórico de teste, que possui o mesmo comprimento que o horizonte de previsão da ferramenta (20 semanas).


## Planejamento
O projeto deve ser realizado em 2 meses. Está prevista uma sessão de design thinking para o entendimento e a passagem de conhecimento entre os especialistas do negócio e a equipe de cientistas de dados (representada pelo PO).
* Semana 1: entendimento de negócio, sessões de transferencia de conhecimento e planejamento desenho da solução.
* Semana 2-6: ciclos de desenvolvimento da solução inicial (sprints).
* Semana 7: geração de relatórios e documentação.
* Semana 8: apresentação dos resultados finais e transferência de conhecimento.

## Arquitetura

* Dados:
  * Os dados são entregues através de 3 arquivos CSV, lidos de uma conexão FTP. Os dados coletados são processados para saneamento e avaliação da sua qualidade.
  * A série histórica possui aproximadamente 2 anos.
  * São coletadas 10 variáveis exógenas.

* Modelos:
  * Será desenvolvido um modelo de auto ML para a previsão das séries temporais.
  * Os modelos serão desenvolvidos utilizando o Azure ML.
  * O treinamento dos modelos aproveitará a tecnologia Spark via utilização do ambiente Databricks.

* Relatórios:
  * Os relatórios serão feitos após o processamento do treinamento dos modelos.
  * Os relatórios são disponibilizados como exportações HTML dos notebooks utilizados.



## Comunicação
* Equipe de desenvolvimento com reuniões diárias em modelo Scrum.
* Reuniões de status executivos a cada 3 semanas.
* Pontos de contato:
  * Retail Co.: Soares
  * Consultoria: Thiago
