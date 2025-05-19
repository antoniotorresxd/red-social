#!/bin/sh
# Salir si algo falla
set -e


# Aplicar migraciones
python manage.py makemigrations --settings=config.settings.local
python manage.py migrate --settings=config.settings.local


echo "Running server..."
python manage.py runserver 0.0.0.0:8003 --settings=config.settings.local