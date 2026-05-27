# Detecção de Phishing com Machine Learning

Projeto de Ciência de Dados aplicado à Cibersegurança para classificação de URLs como legítimas ou phishing utilizando Machine Learning, FastAPI e Docker.

O projeto cobre todo o pipeline de desenvolvimento:

* análise exploratória dos dados;
* pré-processamento;
* engenharia e seleção de features;
* treinamento e comparação de modelos;
* avaliação orientada a métricas de segurança;
* criação de uma API REST;
* containerização com Docker.

## 1. Objetivo

O objetivo do projeto foi investigar se características estruturais de URLs e páginas web são suficientes para identificar ataques de phishing com bom desempenho.

O trabalho buscou responder às seguintes questões:

* É possível detectar URLs de phishing com alta capacidade de generalização?
* Quais características estruturais possuem maior relevância na classificação?
* Como diferentes algoritmos de classificação se comportam nesse problema?
* Uma abordagem simplificada utilizando apenas features estruturais da URL mantém desempenho aceitável para uso em produção?


## 2. Contexto do Problema

Phishing é uma das técnicas mais utilizadas em ataques cibernéticos modernos, normalmente envolvendo:

* roubo de credenciais;
* engenharia social;
* falsificação de páginas;
* redirecionamento para sites maliciosos.

Neste contexto, falsos negativos possuem alto custo:

> uma URL maliciosa classificada como legítima representa um risco real ao usuário.

Por esse motivo, métricas como Recall, F1-Score e ROC-AUC foram priorizadas durante a avaliação dos modelos.


## 3. Estrutura do Projeto

```text
phishing-machine-learning-cyber/
├── api/
│   ├── main.py
│   ├── predictor.py
│   ├── schemas.py
│   └── requirements.txt
│
├── data/
│   ├── dataset.csv
│   ├── dictionary.md
│   ├── output/
|   |     ├── models/
|   |     └── test_train/
|   |
│   └── output_API/
|         ├── models/
|         └── test_train/
|
├── module/
│   ├── __init__.py
│   └── feature_extractor.py
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessamento.ipynb
│   ├── 03_modelagem.ipynb
│   ├── 04_modelagemURL.ipynb
│   ├── 05_avaliacao.ipynb
│   ├── 06_avaliacaoURL.ipynb
│   ├── 07_comparacao_final.ipynb
│   └── 08_testingURL.ipynb
│
├── Dockerfile
├── .gitignore
├── .dockerignore
└── README.md
```

---

## 4.Pipeline Analítico

### `01_eda.ipynb` — Análise Exploratória

Etapa inicial de compreensão dos dados:

* inspeção estrutural do dataset;
* verificação de valores ausentes;
* análise estatística;
* distribuição da variável alvo (`CLASS_LABEL`);
* análise de correlação;
* identificação de possíveis outliers.

O dataset apresentou:

* 10.000 registros;
* classes balanceadas;
* ausência de valores ausentes.

---

### `02_preprocessamento.ipynb` — Pré-processamento

Nesta etapa foram realizados:

* remoção de colunas irrelevantes;
* separação treino/teste;
* preparação das variáveis;
* padronização para modelos sensíveis à escala.

A padronização foi aplicada apenas à Regressão Logística, pois modelos baseados em árvores não necessitam de normalização.

Também foram persistidos artefatos para reprodutibilidade:

* X_train;
* X_test;
* y_train;
* y_test;
* datasets escalonados;
* scaler.


### `03_modelagem.ipynb` — Modelagem Completa

Treinamento utilizando o conjunto completo de variáveis.

Modelos avaliados:

* Regressão Logística;
* Decision Tree;
* Random Forest.

A otimização de hiperparâmetros foi realizada com:

* GridSearchCV;
* validação cruzada (`cv=5`);
* F1-Score como métrica principal de otimização.

O objetivo foi buscar equilíbrio entre:

* Recall;
* Precisão;
* robustez do classificador.

---

## 4) 04_modelagemURL.ipynb — Modelagem URL-Only

Foi criada uma segunda abordagem utilizando apenas features estruturais extraídas diretamente da URL.

O objetivo desta etapa foi construir uma solução:

* mais leve;
* mais rápida;
* facilmente utilizável em APIs e aplicações em tempo real.

As features utilizadas incluem:

* quantidade de pontos;
* subdomínios;
* tamanho da URL;
* hífens;
* caracteres especiais;
* uso de HTTPS;
* presença de IP;
* tamanho do hostname;
* tamanho do path;
* query string;
* double slash;
* entre outras.

---

## 5) 05_avaliacao.ipynb — Avaliação (Modelo Completo)

Os modelos foram avaliados utilizando:

* Recall;
* Precision;
* F1-Score;
* ROC-AUC;
* matrizes de confusão.

Embora Accuracy também tenha sido observada, ela não foi utilizada como principal métrica de decisão, devido à natureza crítica do problema de segurança.

A análise priorizou principalmente:

* redução de falsos negativos;
* capacidade discriminativa;
* equilíbrio entre Recall e Precision.

---

## 6) 06_avaliacaoURL.ipynb — Avaliação (URL-Only)

Avaliação da versão simplificada baseada apenas em URL.

Resultados obtidos:

| Modelo              | ROC-AUC |
| ------------------- | ------- |
| Regressão Logística | 0.9143  |
| Decision Tree       | 0.8708  |
| Random Forest       | 0.9629  |

O modelo Random Forest apresentou o melhor equilíbrio entre:

* Recall;
* F1-Score;
* ROC-AUC.

Mesmo utilizando apenas features estruturais da URL.

---

# 📊 Comparação Final

A comparação entre:

* modelo completo;
* modelo URL-only;

mostrou que houve perda moderada de desempenho ao remover variáveis adicionais, porém a abordagem simplificada manteve excelente capacidade preditiva.

A redução de complexidade tornou o modelo URL-only adequado para:

* APIs;
* sistemas em tempo real;
* integração com aplicações web;
* deploy simplificado.

---

# ⚠️ Insight Importante Obtido

Durante os testes finais foi observado que URLs semanticamente suspeitas podem não ser classificadas como phishing caso sua estrutura seja relativamente simples.

Exemplo:

```text
http://paypal-login-security-update.com
```

Isso ocorre porque o modelo trabalha principalmente com:

* padrões estruturais;
* características léxicas;
* heurísticas da URL.

Sem realizar:

* análise semântica;
* reputacional;
* conteúdo HTML;
* WHOIS;
* DNS;
* certificados SSL.

---

# 🤖 Modelo Utilizado na API

A API utiliza:

```text
Random Forest URL-Only
```

Modelo serializado em:

```text
data/output_API/models/rf_model_url.pkl
```

---

# 🌐 API REST

A inferência foi disponibilizada utilizando FastAPI.

## Endpoint

```http
POST /predict
```

## Requisição

```json
{
  "url": "https://example.com/login"
}
```

## Resposta

```json
{
  "url": "https://example.com/login",
  "prediction": "Legítima",
  "legitimate_probability": 82.0,
  "phishing_probability": 18.0,
  "risk_level": "Baixo Risco"
}
```

---

# 🧩 Camada Heurística de Risco

Além da classificação do modelo, foi implementada uma camada heurística para transformar probabilidades em níveis interpretáveis de risco.

Critérios utilizados:

| Probabilidade de phishing | Nível          |
| ------------------------- | -------------- |
| < 0.30                    | Baixo Risco    |
| 0.30 até < 0.60           | Risco Moderado |
| ≥ 0.60                    | Alto Risco     |

---

# 🔎 Extração de Features

A extração de atributos estruturais foi implementada em:

```text
module/feature_extractor.py
```

O módulo realiza:

* parsing da URL;
* extração léxica;
* análise estrutural;
* identificação de padrões suspeitos.

---

# 🐳 Docker

O projeto foi containerizado utilizando Docker.

## Build

```bash
docker build -t phishing-api .
```

## Execução

```bash
docker run -p 8000:8000 phishing-api
```

---

# 📘 Swagger

Após iniciar a aplicação:

```text
http://localhost:8000/docs
```

A documentação interativa da API é gerada automaticamente pelo FastAPI.

---

# 🚀 Execução Local

## Instalação

```bash
pip install -r api/requirements.txt
```

---

## Variáveis de ambiente

```bash
export PYTHONPATH=.
export MODEL_PATH=data/output_API/models/rf_model_url.pkl
```

---

## Execução

```bash
uvicorn api.main:app --reload
```

---

# ⚠️ Limitações

O modelo possui limitações importantes:

* dependência do dataset utilizado;
* possível drift temporal de ataques;
* ausência de análise semântica;
* ausência de reputação/domínio;
* ausência de análise dinâmica da página.

Portanto, o sistema não deve ser interpretado como mecanismo definitivo de proteção, mas sim como um classificador experimental baseado em padrões estruturais.

---

# 🔮 Próximos Passos

Possíveis evoluções:

* deploy cloud;
* monitoramento;
* logs;
* cache;
* autenticação;
* rate limiting;
* extensão de navegador;
* análise semântica;
* integração com bases de reputação;
* análise HTML;
* análise DNS/WHOIS;
* re-treinamento periódico.

---

# 🧠 Áreas Relacionadas

Este projeto está inserido nas áreas de:

* Data Science;
* Machine Learning;
* Cybersecurity;
* ML Engineering;
* AI Engineering.

---

# 👥 Créditos

Projeto acadêmico/prático desenvolvido com foco em aplicação de Machine Learning para detecção de phishing e disponibilização de inferência via API.
