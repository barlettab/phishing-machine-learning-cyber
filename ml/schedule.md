Agora que entendemos que teremos **dois experimentos novos (3A e 3B)**, eu reorganizaria o cronograma para refletir a evolução real do projeto.

# Fase 1 — Projeto Base (Concluído)

## 1. Introdução

✅

## 2. Entendimento do Problema

✅

## 3. Dataset Inicial

✅

### 3.1 Carregamento dos Dados

✅

### 3.2 EDA

✅

* Visão Geral
* Qualidade dos Dados
* Variável Alvo
* Estatísticas Descritivas
* Correlação
* Insights

## 4. Pré-processamento

✅

## 5. Engenharia de Features Inicial

✅

Features originais do dataset.

## 6. Modelagem Inicial

✅

* Decision Tree
* Logistic Regression
* Random Forest

## 7. Avaliação Inicial

✅

## 8. Modelo URL Only

✅

## 9. Avaliação URL Only

✅

---

# Fase 2 — Validação Externa (Concluído)

## 10. Construção do Dataset Externo

✅

Fontes:

* Phishing.Database
* Malicious URLs Dataset

Resultado:

```text
df_final.csv
```

## 11. Validação Externa

✅

Resultado:

```text
Accuracy : 59,33%
Precision: 63,55%
Recall   : 43,77%
F1       : 51,84%
```

## 12. Análise dos Erros

✅

* False Positives
* False Negatives
* Limitações do modelo

---

# Fase 3 — Evolução do Modelo (Em andamento)

## 13. Reestruturação do Projeto

✅

* Organização de pastas
* Models
* Artifacts
* Datasets
* Notebooks V2

---

## 14. Cenário 3A — Mais Dados

### 14.1 Extração das 22 Features do df_final

✅

Aplicar:

```python
extract_features_v1()
```

---

### 14.2 Construção do Dataset Unificado

✅

```text
Dataset Original
+
Dataset Final
```

---

### 14.3 Treinamento RF Unificado

✅

---

### 14.4 Avaliação RF Unificado

✅

---

### 14.5 Comparação com Modelo Original

✅

Pergunta:

> Mais dados melhoram a generalização?

---

## 15. Cenário 3B — Novas Features

### 15.1 Desenvolvimento do feature_extractor_v2

✅

---

### 15.2 Extração das Novas Features

⏳

Aplicar:

```python
extract_features_v2()
```

---

### 15.3 Treinamento RF V2

⏳

---

### 15.4 Avaliação RF V2

⏳

---

### 15.5 Feature Importance

⏳

Pergunta:

> Quais atributos mais contribuem para a detecção?

---

### 15.6 Comparação com RF Original

⏳

Pergunta:

> Novas features melhoram o desempenho?

---

# Fase 4 — Comparação Final

## 16. Benchmark dos Modelos

⏳

Tabela final:

| Modelo       | Dados               | Features   |
| ------------ | ------------------- | ---------- |
| RF Completo  | Dataset Inicial     | URL + HTML |
| RF URL       | Dataset Inicial     | 22         |
| RF Validado  | df_final            | 22         |
| RF Unificado | Original + df_final | 22         |
| RF V2        | df_final            | 40+        |

---

## 17. Discussão dos Resultados

⏳

* Impacto dos dados
* Impacto das features
* Limitações

---

# Fase 5 — Produto

## 18. FastAPI

✅

## 19. Integração Modelo + API

✅

## 20. Protótipo Hi-Fi

✅

---

## 21. Dockerização

⏳

* Dockerfile
* Build da aplicação

---

## 22. Deploy Cloud

⏳

Sugestões:

* Render
* Railway
* Azure

---

## 23. Frontend Final

⏳

Opcional.

---

# Fase 6 — TCC

## 24. Escrita da Metodologia

⏳

## 25. Escrita dos Resultados

⏳

## 26. Conclusão e Trabalhos Futuros

⏳

---

Se eu fosse priorizar agora, faria nesta ordem:

```text
1. Reestruturar pastas
2. Cenário 3A (Mais Dados)
3. Cenário 3B (Novas Features)
4. Comparação Final
5. Docker
6. Deploy
7. Escrita do TCC
```

Porque os experimentos 3A e 3B podem alterar completamente qual modelo será publicado na API e usado no deploy final.
