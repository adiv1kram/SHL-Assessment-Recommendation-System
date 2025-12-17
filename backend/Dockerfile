FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY data/app ./data/app
COPY data/.env ./data/.env
COPY data/shl_catalog.json ./data/shl_catalog.json

WORKDIR /app/data

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "app.main"]
