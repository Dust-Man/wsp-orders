#!/bin/bash

# Esperar a que la base de datos esté lista
./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up"

# Migraciones de la base de datos
echo "Applying database migrations..."
python /code/myshop/manage.py migrate

# Recolectar archivos estáticos
echo "Collecting static files..."
python /code/myshop/manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn myshop.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -