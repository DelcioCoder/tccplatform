#!/bin/bash
set -e

echo "Aplicando migrações..."
python manage.py migrate --no-input

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input --clear

echo "Iniciando o servidor Daphne..."
exec python3 -m daphne -b 0.0.0.0 -p 8000 core_platform.asgi:application
