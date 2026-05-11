#!/bin/sh
set -e
python manage.py migrate --noinput
# После bind-mount ./staticfiles с хоста может быть пустым — один раз собираем статику в образ/том.
if [ ! -d /app/staticfiles/admin ]; then
  DJANGO_USE_FILE_LOG=false python manage.py collectstatic --noinput
fi
exec "$@"
