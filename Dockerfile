# Dockerfile for Capstone AI Pipeline - Production Ready
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application modules
COPY main.py .
COPY auth.py .
COPY data.py .
COPY retrieval.py .
COPY models.py .
COPY analytics.py .

# Copy static files and templates
COPY static/ ./static/

# Create necessary directories
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
