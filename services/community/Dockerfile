FROM python:3.10-slim

# 2. Variables de entorno para mejor performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Directorio de trabajo
WORKDIR /app

# 4. Instalar dependencias del sistema necesarias para psycopg2/Postgres
RUN apt-get update \
  && apt-get install -y gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# 5. Copiar sólo los requirements y luego instalar
COPY src/requirements.txt .
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# 6. Copiar todo el código fuente de tu app Django
COPY src/ .


COPY src/entrypoint.sh .
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]