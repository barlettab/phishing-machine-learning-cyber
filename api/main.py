from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import URLRequest

from api.predictor import predict_url

app = FastAPI(
    title="Phishing Detection API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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