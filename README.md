---

# Projeto de Observabilidade e Análise de Performance com OpenTelemetry, Jaeger e k6

---

## 🚀 Introdução

Este projeto oferece uma demonstração prática de como construir e utilizar uma **ferramenta de observabilidade robusta, baseada em contêineres**, para analisar o desempenho de aplicações sob carga. Nosso objetivo é ir além de "funciona ou não funciona", buscando entender **como** a aplicação se comporta, onde estão seus gargalos e como ela escala em situações de estresse.

Vamos explorar a sinergia entre **k6** para testes de carga, **OpenTelemetry** para instrumentação e **Jaeger** para visualização de traces distribuídos, tudo orquestrado via **Docker Compose**.

## 🎯 Objetivo do Projeto

Nosso propósito central é validar uma solução de observabilidade conteinerizada que permite:

* **Simular tráfego real:** Usando o k6 para gerar carga controlada e coletar métricas de performance.
* **Instrumentar a aplicação:** Com OpenTelemetry, para que ela "fale" sobre seu próprio desempenho, gerando traces.
* **Visualizar o fluxo de requisições:** Através do Jaeger, para mapear o caminho completo de cada requisição e identificar latências exatas em cada etapa.

Em resumo, queremos demonstrar, com dados concretos, como uma aplicação se comporta sob pressão e como diagnosticar problemas de performance de forma eficiente.

## 🛠️ Ferramentas Utilizadas

Confira as tecnologias que impulsionam este projeto:

* **Docker:** Para empacotar e isolar cada parte da nossa solução em contêineres.
* **Docker Compose:** Para orquestrar e gerenciar a execução de múltiplos contêineres como um único ambiente.
* **k6:** Nosso testador de carga, que simula o tráfego de usuários e coleta métricas de performance.
* **OpenTelemetry:** O padrão de instrumentação que nos ajuda a gerar traces, métricas e logs de forma agnóstica.
* **Jaeger:** O sistema de tracing distribuído que visualiza o caminho das requisições, revelando gargalos.

## 📂 Estrutura do Projeto

Veja como o projeto está organizado:

```
P_TS/
├── docker-compose.yml
├── load_test.js
└── your_python_app/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

### Detalhes dos Componentes:

* **`docker-compose.yml`**: Define e orquestra os serviços (`jaeger` e `your-application`), suas dependências, redes e variáveis de ambiente.
    * **Características:** Orquestra múltiplos serviços; facilita comunicação entre contêineres; mapeia portas para acesso externo; garante ordem de inicialização; suporta OTLP.
* **`load_test.js`**: O script JavaScript para o k6, que dita o comportamento do teste de carga.
    * **Características:** Define o perfil de carga; faz requisições HTTP GET; valida as respostas da aplicação (status, conteúdo, tempo); simula comportamento realista com pausas.
* **`your_python_app/`**: Contém o código da aplicação Python.
    * **`Dockerfile`**: Instruções para construir a imagem Docker da aplicação.
        * **Características:** Define imagem base; copia e instala dependências; expõe porta; define comando de inicialização.
    * **`app.py`**: O código-fonte da aplicação Flask.
        * **Características:** Define o nome do serviço para Jaeger; configura o OpenTelemetry para traces; usa OTLP Exporter; instrumenta Flask e `requests` automaticamente; inclui um endpoint `/` com chamada externa (para `google.com`) para demonstrar latência.
    * **`requirements.txt`**: Lista as dependências Python da aplicação.
        * **Características:** Inclui **`Flask`** (web framework), **`requests`** (requisições HTTP), **`opentelemetry-sdk`** (core do OTel), **`opentelemetry-exporter-jaeger`** (exporter Thrift legado), **`opentelemetry-instrumentation-flask`** (instrumenta Flask), **`opentelemetry-instrumentation-requests`** (instrumenta `requests`), **`deprecated`** (utilitário), e **`opentelemetry-exporter-otlp`** (exporter moderno via OTLP).

## 🚀 Como Rodar o Projeto

Siga estes passos simples para colocar o ambiente em funcionamento:

1.  **Navegue até o diretório raiz** (`P_TS/`) no seu terminal.

2.  **Inicie os Serviços:**
    ```bash
    docker compose up --build -d
    ```
    Isso vai construir (se necessário) e iniciar o Jaeger e sua aplicação em segundo plano.

3.  **Acesse a Interface do Jaeger:**
    Abra seu navegador e vá para: `http://localhost:16686`

4.  **Opcional: Acesse sua Aplicação:**
    Se quiser ver a aplicação funcionando diretamente, acesse: `http://localhost:8000/` (assumindo o mapeamento `8000:8080` no `docker-compose.yml`).

5.  **Execute o Teste de Carga com k6:**
    No terminal, execute:
    ```bash
    cat load_test.js | docker run --rm -i --network p_ts_app-network grafana/k6 run -
    ```
    Isso iniciará o teste de estresse contra sua aplicação conteinerizada.

6.  **Analise os Resultados:**
    * Observe o relatório do k6 no terminal para métricas agregadas (latência média, RPS, falhas).
    * No Jaeger, selecione `my-python-flask-app` em "Service" e clique em "Find Traces" para inspecionar cada requisição e identificar gargalos (por exemplo, a latência introduzida pela chamada ao Google).

## 📊 Análise de Resultados e Observações Chave

Os resultados obtidos através do k6 e do Jaeger fornecem uma visão clara do comportamento da aplicação sob carga. O k6 apresenta métricas agregadas como a duração das requisições (`http_req_duration`) e o volume de requisições por segundo (`http_reqs`), indicando a capacidade geral do sistema.

Complementarmente, o Jaeger detalha o fluxo de cada requisição através de **traces**, que são compostos por **spans**. Cada span representa uma operação dentro da requisição, mostrando seu tempo de execução. Esta granularidade é crucial para identificar com precisão onde o tempo está sendo gasto, como em chamadas para serviços externos (ex: `https://www.google.com`), que podem introduzir latência significativa e se tornarem gargalos.

Em suma, este setup permite não apenas quantificar o desempenho, mas também diagnosticar qualitativamente as causas-raiz de qualquer degradação de performance, facilitando otimizações futuras.

---
