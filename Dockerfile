# Use a slim Python image
FROM python:3.12-slim

WORKDIR /app

# System deps (if needed) and security updates
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates curl && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Northflank will pass PORT; default to 8080 for local runs
ENV PORT=8080
EXPOSE 8080

# Start the HTTP server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]