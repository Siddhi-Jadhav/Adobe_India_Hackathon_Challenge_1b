# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.11-slim

# Set workdir
WORKDIR /app

# Copy and install dependencies
COPY extract_outline.py . 

RUN pip install --no-cache-dir PyMuPDF

# Create input/output directories
RUN mkdir -p /app/input /app/output

# Entry point
CMD ["python", "extract_outline.py"]
