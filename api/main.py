from fastapi import FastAPI

from schemas import URLRequest

from predictor import predict_url


app = FastAPI(
    title="Phishing Detection API"
)


@app.get("/")
def home():

    return {
        "message":
        "API de detecção de phishing ativa"
    }


@app.post("/predict")
def predict(data: URLRequest):

    result = predict_url(data.url)

    return result