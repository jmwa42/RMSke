FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt

# copy Django project (ensure manage.py is at backend/manage.py)
COPY backend /app/backend

WORKDIR /app/backend

# port
EXPOSE 8000

# run migrations then gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn backend.rentals_backend.wsgi:application --bind 0.0.0.0:8000"]

