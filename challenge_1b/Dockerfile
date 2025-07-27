# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    setuptools \
    wheel \
    && pip install --no-cache-dir \
    PyMuPDF==1.23.7 \
    scikit-learn==1.4.0 \
    numpy==1.26.4

COPY run.py .

RUN mkdir -p /app/input /app/output

CMD ["python", "run.py"]