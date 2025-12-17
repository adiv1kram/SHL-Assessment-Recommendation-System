FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements-ultra-minimal.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY data/app ./data/app

# Create data directory and sample catalog
RUN mkdir -p ./data && \
    echo '[{"name":"Python Programming","url":"https://shl.com/python","description":"Python coding assessment","test_type":["Technical"],"duration":"45","adaptive_support":"Yes","remote_support":"Yes"},{"name":"Java Development","url":"https://shl.com/java","description":"Java programming test","test_type":["Technical"],"duration":"50","adaptive_support":"Yes","remote_support":"Yes"}]' > ./data/shl_catalog.json

# Create empty .env if not exists
RUN touch ./data/.env

WORKDIR /app/data

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "app.main"]
