FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r api/requirements.txt

ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/data/output_API/models/rf_model_url.pkl

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]