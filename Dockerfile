# Use a slim Python image
FROM python:3.12-slim

WORKDIR /app

# System deps
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates curl && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Default to 8080 if PORT isn't set, but allow override
ENV PORT=8080
EXPOSE $PORT

# --- THE FIX IS HERE ---
# We remove the brackets [ ] so it runs in a shell.
# This allows ${PORT} to actually be read from the environment.
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT}