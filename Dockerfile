# Stage 1: Node.js (for WhatsApp bot)
FROM node:18-bullseye AS nodebot

# Install Chromium for Puppeteer
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libexpat1 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxrender1 \
    xdg-utils \
    chromium \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app/bot
COPY bot/package*.json ./
RUN npm install --omit=dev
COPY bot/ .

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Stage 2: Django backend
FROM python:3.11-slim AS django

WORKDIR /app

# Copy backend (with manage.py)
COPY backend/ /app/backend/
COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy bot from first stage
COPY --from=nodebot /app/bot /app/bot

# Set Django envs
ENV DJANGO_SETTINGS_MODULE=backend.rentals_backend.settings
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Start Django + WhatsApp bot
CMD sh -c "python /app/backend/manage.py migrate && \
           (cd /app/bot && node index.js &) && \
           gunicorn backend.rentals_backend.wsgi:application --chdir /app/backend --bind 0.0.0.0:8000"

