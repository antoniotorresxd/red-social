# Dockerfile para producción - services/publications

# 1. Imagen base optimizada
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 2. Instalar dependencias del sistema
RUN apt-get update \
 && apt-get install -y gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 3. Instalar dependencias Python
COPY src/requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 4. Copiar todo el código fuente
COPY src/ .

RUN adduser --disabled-password --no-create-home appuser
USER appuser

# 6. Exponer el puerto de producción
EXPOSE 8002

# 7. Arranque por gunicorn en modo producción
CMD ["gunicorn", "--bind", "0.0.0.0:8002", "config.wsgi:application"]
