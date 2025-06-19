FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SITE_ROOT=/srv/mon-site

RUN apt-get update && apt-get install -y \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && mkdir -p "$SITE_ROOT"
VOLUME ["$SITE_ROOT"]

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]