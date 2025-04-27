#!/bin/bash

DJANGO_ENV=$(echo "${DJANGO_ENV}" | tr -d '\r' | xargs)

if [[ "${DJANGO_ENV}" != "development" && "${DJANGO_ENV}" != "production" ]]; then
  echo "Error: DJANGO_ENV must be set to 'development' or 'production'. Current value: '${DJANGO_ENV}'"
  exit 1
fi

echo "Loaded environment variables. Running in ${DJANGO_ENV} mode..."

# Start Django application based on DJANGO_ENV
if [ "$DJANGO_ENV" = "development" ]; then
  echo "Running development server..."
  python manage.py migrate
  python manage.py start_grpc
  python manage.py runserver 0.0.0.0:8000
else
  echo "Running production server with Gunicorn..."
  python manage.py collectstatic --noinput
  python manage.py migrate
  python manage.py start_grpc
  gunicorn core.wsgi:application --bind 0.0.0.0:8000
fi