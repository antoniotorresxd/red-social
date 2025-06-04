# Dockerfile para producción - services/users

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Instalar dependencias de sistema
RUN apt-get update \
 && apt-get install -y gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 2. Instalar dependencias Python
COPY src/requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 3. Copiar el código fuente
COPY src/ .

# 4. (Opcional, recomendado) Usuario seguro
RUN adduser --disabled-password --no-create-home appuser
USER appuser

# 5. Exponer el puerto de producción
EXPOSE 8001

# 6. Arranque con gunicorn 
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "config.wsgi:application"]
