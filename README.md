# 🛡️ Detecção de Phishing com Machine Learning

Projeto de ciência de dados + deploy de API para **classificação de URLs como legítimas ou phishing**.

O repositório cobre o ciclo completo:
- exploração e preparação de dados,
- treino e comparação de modelos,
- versão otimizada usando apenas features de URL,
- disponibilização de inferência via **FastAPI** e **Docker**.

---

## 📌 Objetivo

Construir um pipeline reprodutível para responder:

1. É possível classificar URLs maliciosas com alta acurácia?
2. Quais variáveis são mais relevantes para distinguir phishing de legítimas?
3. Qual algoritmo performa melhor entre Regressão Logística, Árvore de Decisão e Random Forest?
4. Uma abordagem simplificada (somente URL) mantém bom desempenho e reduz custo computacional?

---

## 🗂️ Estrutura do projeto

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
│   └── output_API/             # artefatos da modelagem URL-only e API
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

---

## 🧪 Fluxo analítico (notebooks)

### 1) `01_eda.ipynb` — Análise Exploratória
- Carregamento da base e inspeção estrutural.
- Verificação de qualidade de dados (ausentes, distribuição, estatísticas).
- Avaliação da variável alvo (`CLASS_LABEL`) e equilíbrio entre classes.

### 2) `02_preprocessamento.ipynb` — Pré-processamento
- Remoção de colunas não úteis (ex.: identificador).
- Separação `X`/`y` e split treino-teste.
- Escalonamento para modelos sensíveis à escala (ex.: regressão logística).
- Persistência dos conjuntos processados em `data/output/...`.

### 3) `03_modelagem.ipynb` — Treino
- Treino de:
  - Regressão Logística,
  - Decision Tree,
  - Random Forest.
- Ajuste de hiperparâmetros com `GridSearchCV`.

### 4) `04_avaliacao.ipynb` — Avaliação (modelo completo)
- Comparação por métricas: Accuracy, Precision, Recall, F1, ROC-AUC.
- Matrizes de confusão e interpretação de erros (FP/FN).

### 5) `06_avaliacaoURL.ipynb` — Avaliação (URL-only)
- Repetição da avaliação com subconjunto de variáveis extraídas diretamente da URL.
- Geração de artefatos em `data/output_API/...` para consumo da API.

### 6) `07_comparacao_final.ipynb` — Síntese
- Comparação final entre:
  - modelos com conjunto amplo de variáveis,
  - modelos URL-only.
- Discussão de trade-off entre desempenho e custo computacional.

### 7) `08_testingURL.ipynb`
- Testes finais da estratégia URL-only e validações de uso prático.

---

## 🤖 Modelos e artefatos

Modelos serializados (pickle) incluem, entre outros:
- `data/output/models/logistic_regression.pkl`
- `data/output/models/decision_tree.pkl`
- `data/output/models/random_forest.pkl`
- `data/output_API/models/log_model_url.pkl`
- `data/output_API/models/tree_model_url.pkl`
- `data/output_API/models/rf_model_url.pkl` ✅ (utilizado na API)

Também há artefatos auxiliares como scaler e bases de treino/teste salvas para reprodutibilidade.

---

## 🌐 API de predição

A API foi implementada em FastAPI.

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

---

## 🔎 Features de URL usadas pela API

A inferência da API utiliza extração de atributos estruturais implementada em `modules/feature_extractor.py`.

Principais grupos de variáveis:
- Estrutura da URL (pontos, subdomínios, tamanho, níveis de path etc.)
- Sinais de ofuscação/suspeita (`@`, `%`, `#`, números, duplo slash, etc.)
- Uso de HTTPS
- Uso de IP no lugar de domínio
- Presença do domínio em partes incomuns da URL

As features finais usadas em produção estão listadas em `api/predictor.py` (lista `url_features`).

---

## 🚀 Como executar localmente

### Opção A — Python + Uvicorn

#### 1. Instalar dependências
```bash
pip install -r api/requirements.txt
```

#### 2. Definir variáveis de ambiente
```bash
export PYTHONPATH=.
export MODEL_PATH=data/output_API/models/rf_model_url.pkl
```

#### 3. Subir API
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. Acessar
- Docs interativas: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/`

---

### Opção B — Docker

```bash
docker build -t phishing-api .
docker run --rm -p 8000:8000 phishing-api
```

O `Dockerfile` já configura `MODEL_PATH` para:
`/app/data/output_API/models/rf_model_url.pkl`

---

## 📊 Dataset e dicionário

- Base principal: `data/dataset.csv`
- Dicionário de variáveis: `data/dictionary.md`

O dataset contém atributos léxicos e estruturais de URLs/páginas para classificação binária (`CLASS_LABEL`):
- `0` = legítima
- `1` = phishing

---

## ⚠️ Limitações e próximos passos

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

---

## 👥 Créditos

Projeto acadêmico/prático de aplicação de Machine Learning em cibersegurança, com foco em detecção de phishing e disponibilização de inferência via API.
