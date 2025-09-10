# syntax=docker.io/docker/dockerfile:1.7-labs
FROM python:3.11-slim

# --- Environment variables ---
ENV DUO_USE_VENV=false
ENV PYTHONUNBUFFERED=true
ENV PYTHONIOENCODING=utf-8

# --- Working directory ---
WORKDIR /app

# --- Copy the app (excluding heavy directories) ---
COPY \
  --exclude=antiabuse/antiporn \
  --exclude=test \
  --exclude=vm \
  . /app

# --- Install system dependencies ---
RUN apt-get update && apt-get install -y --no-install-recommends \
      ffmpeg \
      curl \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

# --- Install Python dependencies ---
RUN pip install --no-cache-dir -r /app/requirements.txt

# --- Pre-download SpaCy model ---
RUN python -m spacy download en_core_web_sm

# --- Pre-download FireHOL list to avoid runtime memory spikes ---
RUN mkdir -p /tmp/duolicious-firehol \
    && curl -L https://iplists.firehol.org/files/firehol_anonymous.netset \
       -o /tmp/duolicious-firehol/firehol_anonymous.netset

# --- Make startup script executable ---
RUN chmod +x /app/api.main.sh

# --- Entrypoint ---
CMD ["/app/api.main.sh"]
