web: sh -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn Peredelka55.wsgi:application --bind 0.0.0.0:$PORT --workers ${GUNICORN_WORKERS:-3}"
