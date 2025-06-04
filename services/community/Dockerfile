# 1) Imagen base optimizada para producción
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 2) Instalar solo lo necesario del sistema
RUN apt-get update \
 && apt-get install -y gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 3) Instalar dependencias Python
COPY src/requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 4) Copiar el código fuente (TODO el src para prod)
COPY src/ .

RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8002


CMD ["gunicorn", "--bind", "0.0.0.0:8002", "config.wsgi:application"]
