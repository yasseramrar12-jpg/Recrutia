# Image du backend RECRUT'IA (API FastAPI + module IA)
FROM python:3.12-slim

WORKDIR /application

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt "psycopg[binary]>=3.1"

COPY app ./app
COPY seed.py .

EXPOSE 8000
# Crée le compte de démonstration si absent, puis démarre l'API.
CMD ["sh", "-c", "python seed.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
