# Bookworm: supported base; Buster is EOL and breaks apt mirrors.
FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=Peredelka55.settings

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        libjpeg62-turbo zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir -p /app/logs \
    && DJANGO_USE_FILE_LOG=false python manage.py collectstatic --noinput

EXPOSE 8000

# sh: чтобы bind-mount с Windows не требовал executable bit у entrypoint.sh
ENTRYPOINT ["sh", "/app/docker/entrypoint.sh"]
CMD ["sh", "-c", "gunicorn Peredelka55.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-3}"]
