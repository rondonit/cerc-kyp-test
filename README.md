# CERC Take Home Test - KYP Assistant MVP

Esse projeto é um MVP de automação para auxiliar analistas de crédito na entrada de duplicata escritural.

## Tarefas que serão implementadas

[ ] - Tarefa 1: Analyze credit data and financial statements to determine the degree of risk involved in extending credit or lending money.
[ ] - Tarefa 3: Generate financial ratios, using computer programs, to evaluate customers' financial status.
[ ] - Tarefa 4: Prepare reports that include the degree of risk involved in extending credit or lending money.

## Módulos do projeto

- normalize - transforma o JSON em um formato interno
- fin_ratios - calcula índices financeiros
- llm_client - chama a LLM para realizar a análise
- report - gera o relatório
- workflow - orquestra o pipeline

## Dados para teste
Disponível em https://www.kaggle.com/datasets/wbqrmgmcia7lhhq/sec-financial-statement-data-in-json
Usei também Yahoo Finance por meio da API