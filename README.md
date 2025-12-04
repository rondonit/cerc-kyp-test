# CERC Take Home Test - KYP Assistant MVP

Esse projeto é um MVP de automação para auxiliar analistas de crédito na entrada de duplicata escritural, focado em resolver as tarefas propostas no desafio da CERC.

## Tarefas do Desafio Implementadas

O pipeline de automação foi construído para executar em sequência 3 tarefas do desafio O*NET, criando um fluxo de trabalho completo de análise de risco:

1.  **Tarefa 3: Generate financial ratios...**
    *   **Implementação:** Esta etapa é realizada pelo módulo `src/ratios.py`, que recebe os dados financeiros brutos e calcula uma série de indicadores-chave de liquidez, alavancagem, rentabilidade e geração de caixa.

2.  **Tarefa 1: Analyze credit data and financial statements...**
    *   **Implementação:** O coração da análise é o módulo `src/risk_analyst.py`. Ele utiliza IA Generativa (via Gemini ou Ollama) para interpretar os dados da empresa e os indicadores calculados, realizando uma análise qualitativa e quantitativa para determinar o grau de risco.

3.  **Tarefa 4: Prepare reports that include the degree of risk...**
    *   **Implementação:** Ao final do pipeline, o `src/cli.py` e o `src/core.py` orquestram a geração de um relatório completo em formato Markdown. O relatório inclui todos os dados, indicadores e a análise da IA, e é salvo na pasta `reports/`. Adicionalmente, há a opção de gerar uma versão em PDF.

## Fonte dos Dados

Para provar o conceito, os dados financeiros das empresas são extraídos em tempo real da API do **Yahoo Finance**, utilizando a biblioteca `yfinance`. O pipeline foi construído para ser agnóstico à fonte de dados, podendo ser adaptado para consumir dados de APIs internas ou outros provedores.

## Como Usar

### Pré-requisitos
-   Python 3.13 ou superior.
-   [uv](https://github.com/astral-sh/uv) (um instalador e resolvedor de pacotes Python rápido).
-   Uma chave de API para o provedor de LLM escolhido (ex: Google Gemini).

### Configuração

1.  **Clone o repositório e entre na pasta:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd cerc-kyp-test
    ```

2.  **Crie o ambiente virtual e instale as dependências com `uv`:**
    ```bash
    # Este comando cria e ativa o ambiente virtual na pasta .venv
    uv venv

    # Este comando lê o requirements.txt e instala as dependências
    uv sync
    ```

3.  **Configure a Chave da API:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave da API do Gemini:
    ```
    GOOGLE_API_KEY="<sua_chave_aqui>"
    ```

### Executando o Pipeline

A aplicação é executada através da linha de comando.

```bash
uv run -m src.cli --ticket <TICKER> --model <MODELO> [--pdf]
```

**Argumentos:**
*   `--ticket <TICKER>`: **(Obrigatório)** O código da ação da empresa (ex: `AAPL`, `PETR4.SA`).
*   `--model <MODELO>`: **(Opcional)** O modelo de IA a ser usado (`gemini` ou `ollama`). Padrão: `gemini`.
*   `--pdf`: **(Opcional)** Gera uma versão em PDF do relatório.

**Exemplos:**
```bash
# Analisar a Apple com Gemini e gerar relatórios em MD e PDF
uv run -m src.cli --ticket AAPL --model gemini --pdf

# Analisar a Petrobras com Gemini (apenas MD)
uv run -m src.cli --ticket PETR4.SA --model gemini
```

Para processar várias empresas de uma vez, execute o script `fetch_all.sh`:
```bash
./fetch_all.sh
```

### Executando com Docker (via Docker Compose)

A maneira recomendada de executar a aplicação é via Docker Compose, que gerencia o ambiente containerizado. O arquivo `docker-compose.yml` define dois serviços que usam a mesma imagem, mas com finalidades diferentes: `risk-analyzer-api` (para o servidor web) e `risk-analyzer-cli` (para a ferramenta de linha de comando).

1.  **Construa a imagem Docker:**
    *   Este comando precisa ser executado apenas uma vez, ou sempre que o código ou as dependências mudarem.
    ```bash
    docker-compose build
    ```

2.  **Opção A: Rodar como API (Serviço Web):**
    *   **Para iniciar o servidor:**
        ```bash
        # O `-d` inicia o serviço em segundo plano (detached mode)
        docker-compose up -d risk-analyzer-api
        ```
        A API estará disponível em `http://localhost:8000`.

    *   **Para interagir com a API (exemplo com `curl`):**
        ```bash
        # Dispara uma análise para a Apple e retorna o relatório em Markdown
        curl -X POST "http://localhost:8000/analyze/AAPL?model=gemini"
        ```

    *   **Para ver os logs do servidor:**
        ```bash
        docker-compose logs -f risk-analyzer-api
        ```

    *   **Para parar o serviço da API:**
        ```bash
        docker-compose down risk-analyzer-api
        ```

3.  **Opção B: Rodar como Ferramenta de Linha de Comando (CLI):**
    *   Use `docker-compose run --rm risk-analyzer-cli` para execuções únicas. O contêiner será removido após a conclusão.

    *   **Para uma única empresa:**
        ```bash
        docker-compose run --rm risk-analyzer-cli --ticket GOOGL --model gemini --pdf
        ```

    *   **Para processar todas as empresas em lote:**
        ```bash
        docker-compose run --rm risk-analyzer-cli ./fetch_all.sh
        ```

## Funcionalidades Adicionais Implementadas

Além do fluxo básico, foram adicionadas funcionalidades para aumentar a robustez e utilidade da análise:

*   **Pontuação de Confiabilidade dos Dados:** O pipeline analisa a quantidade de dados financeiros disponíveis e calcula uma "pontuação de confiabilidade", que é passada para a IA para que a análise seja mais cautelosa caso os dados sejam incompletos.
*   **Geração de PDF:** A flag `--pdf` permite a conversão do relatório final em um arquivo PDF, facilitando o compartilhamento.

## Próximos Passos (Possíveis Melhorias)

Como este é um MVP, existem várias avenidas para evolução e produção:

-   [x] **Expor via API RESTful (com Flask):** Implementado para permitir a integração com outros sistemas, como o n8n. Para documentação interativa da API, pode-se considerar a integração com bibliotecas como Flask-RESTX.
-   [x] **Containerização com Docker:** A aplicação agora está empacotada em um contêiner Docker para facilitar o deploy e garantir consistência em qualquer ambiente.
-   [ ] **Adicionar Testes:** Implementar testes unitários para as funções de utilitários e de transformação, e testes de integração para o pipeline principal, garantindo a confiabilidade do código.
-   [ ] **Orquestração Avançada:** Para cenários com múltiplos pipelines ou maior complexidade, o orquestrador leve em Python poderia ser migrado para uma ferramenta como **Airflow** ou **Dagster**.
-   [ ] **Cache de Dados:** Implementar um sistema de cache mais robusto (como Redis) para os dados das empresas, evitando chamadas repetidas à API do Yahoo Finance.
