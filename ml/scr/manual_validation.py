from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

from features.feature_extractor_v2 import extract_features

import pandas as pd
import joblib
from pathlib import Path

MODEL_PATH = (
    BASE_DIR /
    "models" /
    "scenario_3c1" /
    "rf_scenario_3c1.pkl"
)

FEATURES_PATH = (
    BASE_DIR /
    "artifacts" /
    "scenario_3c1" /
    "feature_columns.pkl"
)

PHISH_PATH = (
    BASE_DIR /
    "datasets" /
    "validation" /
    "phishing_urls.txt"
)

BENIGN_PATH = (
    BASE_DIR /
    "datasets" /
    "validation" /
    "urls_not_phish.txt"
)

OUTPUT_PATH = (
    BASE_DIR /
    "datasets" /
    "validation" /
    "manual_validation_results.csv"
)


def load_urls(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        return [
            line.strip()
            for line in f
            if line.strip()
        ]


print("=" * 50)
print("Carregando modelo...")
print("=" * 50)

model = joblib.load(MODEL_PATH)

feature_names = joblib.load(
    FEATURES_PATH
)

print("Modelo carregado com sucesso")


phishing_urls = load_urls(PHISH_PATH)
benign_urls = load_urls(BENIGN_PATH)

print(
    f"URLs phishing: {len(phishing_urls)}"
)

print(
    f"URLs benignas: {len(benign_urls)}"
)


urls = phishing_urls + benign_urls

real_labels = (
    [1] * len(phishing_urls)
    +
    [0] * len(benign_urls)
)


print("=" * 50)
print("Extraindo features...")
print("=" * 50)

features = [
    extract_features(url)
    for url in urls
]

df_features = pd.DataFrame(features)

X = df_features[
    feature_names
]

print(
    f"Shape features: {X.shape}"
)


print("=" * 50)
print("Realizando predições...")
print("=" * 50)

predictions = model.predict(X)

print(
    pd.Series(predictions)
    .value_counts()
)

from sklearn.metrics import (
    confusion_matrix,
    classification_report
)

print("\nClassification Report")
print(
    classification_report(
        real_labels,
        predictions
    )
)

print("\nConfusion Matrix")
print(
    confusion_matrix(
        real_labels,
        predictions
    )
)

probabilities = model.predict_proba(X)


results = df_features.copy()

results["url"] = urls

results["real_label"] = real_labels

results["predicted_label"] = predictions

results["prob_benign"] = probabilities[:, 0]

results["prob_phishing"] = probabilities[:, 1]


results["correct"] = (
    results["real_label"]
    ==
    results["predicted_label"]
)

# False Positives
fp = results[
    (results["real_label"] == 0)
    &
    (results["predicted_label"] == 1)
]

# False Negatives
fn = results[
    (results["real_label"] == 1)
    &
    (results["predicted_label"] == 0)
]

fp.to_csv(
    BASE_DIR /
    "datasets" /
    "validation" /
    "false_positives.csv",
    index=False
)

fn.to_csv(
    BASE_DIR /
    "datasets" /
    "validation" /
    "false_negatives.csv",
    index=False
)

print(f"False Positives: {len(fp)}")
print(f"False Negatives: {len(fn)}")

accuracy = (
    results["correct"]
    .mean()
)

print("\nRESULTADO FINAL")
print("=" * 50)

print(
    f"Accuracy: {accuracy:.4f}"
)

print(
    f"Acertos: {results['correct'].sum()}"
)

print(
    f"Erros: {(~results['correct']).sum()}"
)

print("=" * 50)

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"Arquivo salvo em:\n{OUTPUT_PATH}"
)