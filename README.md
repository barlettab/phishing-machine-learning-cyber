# Detecção de Phishing com Machine Learning

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-4CAF50?style=flat-square)

</div>

Projeto de ciência de dados + deploy de API para **classificação de URLs como legítimas ou phishing**.

## 1. Introdução

O *phishing* continua a ser uma das principais e mais dinâmicas vetores de ataques cibernéticos do mundo, explorando a engenharia social para enganar usuários e roubar credenciais confidenciais, dados financeiros ou infectar redes corporativas. Tradicionalmente, as soluções de segurança dependem de duas abordagens extremas: ou utilizam listas estáticas de bloqueio (*blacklists*) — que falham ao tentar detectar ameaças novas criadas em minutos —, ou exigem o carregamento e varredura completa do código HTML da página, o que introduz um alto custo computacional, atraso na resposta (*network overhead*) e riscos de segurança para os próprios servidores de análise.

Este projeto propõe o desenvolvimento de um pipeline inteligente de Machine Learning voltado para a classificação automatizada e em tempo real de URLs maliciosas. Ele aborda o problema sob duas perspectivas de engenharia de dados: um cenário analítico convencional baseado em informações completas da página (incluindo o código-fonte) e um cenário de produção otimizado (*URL-only*), capaz de classificar riscos instantaneamente antes mesmo de o usuário estabelecer conexão com o site suspeito.

## 2. Objetivos do Projeto

O propósito central deste trabalho é avaliar a viabilidade e o custo-benefício de implementar um sistema inteligente e ágil de segurança cibernética. De forma detalhada, os objetivos dividem-se em:

* **Desenvolver um Pipeline End-to-End de Classificação:** Realizar o ciclo completo de Ciência de Dados, desde a análise exploratória (EDA) e pré-processamento rigoroso de um dataset com 10.000 amostras equilibradas, até o treinamento, tunagem e avaliação de algoritmos de aprendizado supervisionado (Regressão Logística, Decision Tree e Random Forest).
  
* **Mapear Padrões de Ofuscação de URLs:** Identificar estatisticamente quais atributos textuais (como contagem de pontos, comprimento do caminho, subdomínios, presença de endereços IP diretos e termos sensíveis) carregam maior poder discriminatório na separação de links legítimos e maliciosos.
  
* **Avaliar o Trade-off entre Robustez e Latência:** Conduzir um experimento comparativo para quantificar a perda de desempenho preditivo ao remover completamente os recursos ricos obtidos do HTML das páginas, avaliando se a análise exclusiva da string da URL sustenta métricas estatísticas robustas (como ROC-AUC e Recall).
  
* **Construir um Protótipo de Produção Otimizado:** Implementar um módulo funcional e modular de extração sintática de características (`feature_extractor.py`) integrado a uma API em **FastAPI** de baixíssima latência, simulando regras de negócio acionáveis e níveis de risco para tomada de decisão automatizada em tempo real.

## 3. Estrutura do projeto

```text
phishing-machine-learning-cyber/
├── api/
│   ├── main.py                 # endpoints FastAPI
│   ├── predictor.py            # carga do modelo e predição
│   ├── schemas.py              # schema da requisição
│   └── requirements.txt        # dependências
├── data/
│   ├── dataset.csv             # base principal
│   ├── dictionary.md           # dicionário de dados
│   ├── output/                 # artefatos da modelagem completa
│   |     ├── models/
|   |     └── train_test/
│   └── output_API/             # artefatos da modelagem URL-only e API
│   |     ├── models/
|   |     └── train_test/
├── modules/
│   └── feature_extractor.py    # extração de features estruturais da URL
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessamento.ipynb
│   ├── 03_modelagem.ipynb
│   ├── 04_avaliacao.ipynb
│   ├── 06_avaliacaoURL.ipynb
│   ├── 07_comparacao_final.ipynb
│   └── 08_testingURL.ipynb
└── Dockerfile
```
## 4. Dataset e dicionário

- Base principal: `data/dataset.csv`
- Dicionário de variáveis: `data/dictionary.md`

O dataset contém atributos léxicos e estruturais de URLs/páginas para classificação binária (`CLASS_LABEL`):
- `0` = legítima
- `1` = phishing

## 5. Notebooks 

### 🥎 `01_eda.ipynb` — Análise Exploratória
O objetivo principal desta etapa é compreender a estrutura geral do dataset para direcionar os passos seguintes relacionados ao pré-processamento e a modelagem preditiva.

#### Achados na EDA:
  - **Dimensões:** 10.000 registros e 50 atributos.
  - **Tipos de Dados:** Composto por 47 variáveis do tipo `int64` e 3 variáveis `float64`.
  - **Integridade:** Dados altamente consistentes com 0% de valores ausentes e zero duplicados.
  - O dataset possui exatamente 5.000 registros de URLs legítimas e 5.000 registros de URLs fraudulentas.
  - O balanceamento de 50/50 elimina a necessidade de técnicas de reamostragem e evita vieses no modelo.
  - A variável `HttpsInHostname` apresenta o mesmo valor em todo o dataset, não possuindo poder discriminatório.

### 🥎 `02_preprocessamento.ipynb` — Pré-processamento
O objetivo central é aplicar tratamentos estruturais e transformações nos dados identificados na fase de análise exploratória (EDA). As ações principais incluem:
  - Remover variáveis irrelevantes ou sem variabilidade.
  - Separar as variáveis explicativas (features) da variável alvo (target).
  - Dividir o conjunto de dados em subconjuntos de treino (80%) e teste (20%) de forma estratificada.
  - Aplicar normalização de escala nas variáveis para atender a modelos específicos (como Regressão Logística).
  - Exportar e salvar os conjuntos finais processados e o objeto do escalonador (scaler) para uso futuro.

### 🥎 `03_modelagem.ipynb` — Treino com todas as features
O propósito central desta etapa é aplicar algoritmos de Machine Learning para a classificação binária de URLs (legítimas vs. maliciosas). Dessa forma, foram escolhidos três algoritmos distintos devido às suas características complementares de estrutura, interpretabilidade e generalização:

  - **Regressão Logística:** Utilizada como o modelo linear de base (baseline). Serve para testar se o problema pode ser resolvido assumindo que o efeito dos atributos é puramente proporcional ou aditivo (ex: quanto maior o comprimento da URL, maior a chance de ser ataque). Este modelo foi alimentado com os dados normalizados pelo StandardScaler.
    
  - **Decision Tree**: Escolhida por sua alta interpretabilidade e capacidade de criar regras hierárquicas não lineares e comportamentos mais complexos entre os atributos estruturais das páginas.

  - **Random Forest**: Implementada como uma abordagem robusta de ensemble (conjunto de árvores) orientada a maximizar a capacidade de generalização e mitigar riscos de overfitting inerentes a uma única árvore.

*Observação: O notebook realiza o salvamento sistemático de todos os modelos ajustados utilizando a biblioteca joblib. Os arquivos gerados são direcionados para a pasta de saídas do projeto (../data/output/models/).*

### 🥎  `04_avaliacao.ipynb` — Avaliação (modelo completo)
Esta etapa propõe em mensurar e comparar o desempenho dos modelos de classificação ajustados anteriormente através da comparação por métricas, matrizes de confusão e interpretação de erros (FP/FN).

#### Resultados das Métricas 

| Modelo | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | **0.9860** | **0.9841** | **0.9880** | **0.9860** | **0.9990** |
| **Decision Tree** | 0.9650 | 0.9678 | 0.9620 | 0.9649 | 0.9649 |
| **Regressão Logística** | 0.9520 | 0.9593 | 0.9440 | 0.9516 | 0.9841 |

###  🥎 `05_modelagemURL.ipynb` — Treino somente com as features associadas à URL
Realizar o treinar os mesmos algoritmos de Machine Learning utilizando apenas atributos extraídos diretamente da URL, desconsiderando completamente as variáveis dependentes da análise estrutural ou do código HTML da página web. E dessa forma, avaliar se essa abordagem simplificada é capaz de manter um bom poder preditivo para ser aplicada em sistemas de monitoramento leve ou APIs de classificação automática de alto desempenho.

*Observação: O notebook realiza o salvamento final de novos conjuntos de dados específicos e normalizados (como X_train_scaled_url.csv e X_test_scaled_url.csv) direcionados para uma pasta chamada ../data/output_API/.*

### 🥎 `06_avaliacaoURL.ipynb` — Avaliação (URL-only)
Avalia* os modelos preditivos sob a restrição de utilizar exclusivamente atributos extraídos das strings das URLs, ignorando por completo qualquer informação vinda do HTML das páginas.

#### Resultados das Métricas 

| Modelo | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | **0.900** | **0.8861** | **0.9180** | **0.9018** | **0.9626** |
| **Decision Tree** | 0.8695 | 0.8516 | 0.8950 | 0.8727 | 0.8708 |
| **Regressão Logística** | 0.8500 | 0.8314 | 0.8780 | 0.8541 | 0.9143 |

O notebook conclui textualmente que os resultados evidenciam que os atributos textuais da URL conseguem segurar padrões muito relevantes do comportamento de phishing. Isso valida a hipótese inicial: é totalmente viável construir uma API ultraleve e de baixíssima latência para produção, abrindo mão do HTML para ganhar velocidade e economia computacional massiva.

### 🥎 `07_comparacao_final.ipynb` — Síntese
Quantificar o custo-benefício de simplificar o sistema comparando os dois cenários de modelagem verificando o desempenho de cada algoritmo operando com e sem as features associadas ao código HTML das páginas. 

#### Resultados 
- A redução drástica no volume de atributos causou um impacto surpreendentemente pequeno sobre o desempenho preditivo dos algoritmos. 

- O modelo Random Forest consolidou-se como o melhor algoritmo e o mais resiliente do projeto: ele sofreu uma perda de apenas 3,61% no seu índice ROC-AUC (passando de 0.9990 no modelo completo para 0.9629 no modelo restrito apenas às URLs). Isso prova que a maior parte da inteligência discriminatória do problema já reside na própria composição da string do link.

- No cenário restrito da URL, o modelo Random Forest manteve um Recall de 91,80% (em comparação aos 98,40% obtidos no cenário completo). Isso significa que, mesmo sem gastar recursos para abrir ou ler uma linha sequer do HTML do site malicioso, o modelo ainda consegue blindar o sistema identificando corretamente 9 em cada 10 ataques de phishing.

- Além da velocidade, isso adiciona uma camada de segurança física, pois o pipeline analisa apenas o texto fornecido (string), mitigando o risco de executar ou carregar códigos maliciosos na infraestrutura automatizada durante a varredura.

### 🥎 `08_testingURL.ipynb`
- Apresenta a etapa de teste prático e simulação em produção da abordagem otimizada (que utiliza exclusivamente os atributos extraídos da string da URL).

## 6. Modelos e artefatos gerados nos Notebooks

Modelos serializados (pickle) incluem, entre outros:
- `data/output/models/logistic_regression.pkl`
- `data/output/models/decision_tree.pkl`
- `data/output/models/random_forest.pkl`
- `data/output_API/models/log_model_url.pkl`
- `data/output_API/models/tree_model_url.pkl`
- `data/output_API/models/rf_model_url.pkl` 

Também há artefatos auxiliares como scaler e bases de treino/teste salvas para reprodutibilidade.

## 7. Script de Extração de Feature 
O objetivo central deste arquivo `modules/feature_extractor.py`  é funcionar como a camada de processamento de dados (Engenharia de Recursos) em tempo real para a API do projeto. Ele transforma uma string de texto bruto (o link) num dicionário numérico padronizado que os modelos de Machine Learning conseguem interpretar e classificar instantaneamente. O código analisa as características sintáticas da URL sem efetuar nenhuma requisição HTTP à internet, o que garante máxima velocidade e segurança computacional ao pipeline.

## 8. API de predição de URL fraudulentas

A API foi implementada em FastAPI que recebe a URL bruta, importa o script `feature_extractor.py`, carrega o modelo Random Forest treinado com atributos exclusivos de URL e expõe regras de negócio acionáveis no retorno JSON.

### Endpoint de status
- `GET /`
- Retorno: mensagem indicando API ativa.

### Endpoint de inferência
- `POST /predict`
- Body (JSON):

```json
{
  "url": "https://exemplo.com/login"
}
```

### Resposta esperada
- URL avaliada
- classificação (`Legítima`, `Suspeita`, `Phishing`)
- probabilidades de classe
- nível de risco (`Baixo Risco`, `Risco Moderado`, `Alto Risco`)

A classificação de risco é baseada na probabilidade prevista de phishing:
- `< 0.30` → Baixo Risco
- `0.30 a < 0.60` → Risco Moderado
- `>= 0.60` → Alto Risco

## 9. Features de URL usadas pela API

A inferência da API utiliza extração de atributos estruturais implementada em `modules/feature_extractor.py`.

Principais grupos de variáveis:
- Estrutura da URL (pontos, subdomínios, tamanho, níveis de path etc.)
- Sinais de ofuscação/suspeita (`@`, `%`, `#`, números, duplo slash, etc.)
- Uso de HTTPS
- Uso de IP no lugar de domínio
- Presença do domínio em partes incomuns da URL

As features finais usadas em produção estão listadas em `api/predictor.py` (lista `url_features`).

## 10. Como executar a API localmente

### Opção A — Python + Uvicorn

#### 1º Passo: Instalar dependências
```bash
pip install -r api/requirements.txt
```

#### 2º Passo: Definir variáveis de ambiente
```bash
export PYTHONPATH=.
export MODEL_PATH=data/output_API/models/rf_model_url.pkl
```

#### 3º Passo: Subir API
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### 4º Passo: Acessar
- Docs interativas: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/`

### Opção B — Docker

```bash
docker build -t phishing-api .
docker run --rm -p 8000:8000 phishing-api
```

O `Dockerfile` já configura `MODEL_PATH` para:
`/app/data/output_API/models/rf_model_url.pkl`

## 11. Containerização com Docker

Para isolar a API de predição, garantir a reprodutibilidade dos resultados e mitigar riscos de conflitos de dependências em produção (como divergências de versões do Scikit-Learn entre ambientes), a aplicação foi empacotada utilizando o **Docker**.

A imagem foi configurada a partir de uma distribuição leve do Python (`python:3.10-slim`), minimizando o tamanho final do artefato de deploy e reduzindo a superfície de vulnerabilidades do servidor.

## 12. Limitações e próximos passos

### Limitações
- Dependência de um dataset específico.
- Possível drift temporal de padrões de phishing.
- Abordagem majoritariamente estática (características da URL).

### Próximos passos sugeridos
- Validação externa com novas bases.
- Rotina de monitoramento e re-treino periódico.
- Feature store/versionamento formal de modelos.
- Deploy com observabilidade (logs, métricas, alertas).
- Criação de extensão de navegador ou integração com gateway de segurança.

## 13. Créditos

Projeto prático de aplicação de Machine Learning em cibersegurança, com foco em detecção de phishing e disponibilização de inferência via API.
