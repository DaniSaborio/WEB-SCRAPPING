FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema (para psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    chromium \
    chromium-driver \
    libnss3 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libatk1.0-0 \
    libnss3 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
 && rm -rf /var/lib/apt/lists/*

# Requisitos de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos backend (API + scrapper) y frontend
COPY api/ ./api/
COPY frontend/ ./frontend/

# Opcional: si quieres tener main.py/scheduler.py dentro también
COPY main.py scheduler.py ./ 

# Variables por defecto (se sobreescriben en docker-compose)
ENV PG_HOST=db \
    PG_PORT=5432

WORKDIR /app/api

EXPOSE 5000

CMD ["python", "json_api_server.py"]
