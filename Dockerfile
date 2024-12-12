FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt migrations.json ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ ./app

EXPOSE 8000