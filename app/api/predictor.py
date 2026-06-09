import os
import joblib
import pandas as pd
from modules.feature_extractor import extract_features

# =========================
# Carregando modelo
# =========================

MODEL_PATH = os.getenv("MODEL_PATH")

if not MODEL_PATH:
    raise ValueError("MODEL_PATH não definida no ambiente")

rf_model = joblib.load(MODEL_PATH)

# =========================
# Features utilizadas
# =========================

url_features = [

    'NumDots',
    'SubdomainLevel',
    'PathLevel',
    'UrlLength',
    'NumDash',
    'NumDashInHostname',
    'AtSymbol',
    'TildeSymbol',
    'NumUnderscore',
    'NumPercent',
    'NumQueryComponents',
    'NumAmpersand',
    'NumHash',
    'NumNumericChars',
    'NoHttps',
    'IpAddress',
    'DomainInSubdomains',
    'DomainInPaths',
    'HostnameLength',
    'PathLength',
    'QueryLength',
    'DoubleSlashInPath'
]


# =========================
# Predição
# =========================

def predict_url(url):

    features = extract_features(url)

    df = pd.DataFrame([features])

    df = df[url_features]

    probabilities = rf_model.predict_proba(df)[0]

    legit_prob = probabilities[0]
    phishing_prob = probabilities[1]

    # =========================
    # Risco
    # =========================

    if phishing_prob < 0.30:

        risk = "Baixo Risco"
        prediction = "Legítima"

    elif phishing_prob < 0.50:

        risk = "Risco Moderado"
        prediction = "Suspeita"

    else:

        risk = "Alto Risco"
        prediction = "Phishing"

    return {

        "url": url,

        "prediction": prediction,

        "legitimate_probability":
            f"{legit_prob * 100:.2f}%",

        "phishing_probability":
            f"{phishing_prob * 100:.2f}%",

        "risk_level": risk
    }
