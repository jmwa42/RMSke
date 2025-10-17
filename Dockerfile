# =========================
# Stage 1: Node.js (WhatsApp Bot)
# =========================
FROM node:18-bullseye AS nodebot

# Install Chromium dependencies for Puppeteer
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
COPY app/package*.json ./
RUN npm install --omit=dev
COPY bot/ .

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true


# =========================
# Stage 2: Python (Django Backend)
# =========================
FROM python:3.11-slim AS django
WORKDIR /app

# Copy backend files
COPY backend /app/backend
COPY backend/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt gunicorn

# Copy Node bot from previous stage
COPY --from=nodebot /app/bot /app/bot

# Expose port
EXPOSE 8000

# Start Django + WhatsApp bot
CMD sh -c "python backend/manage.py migrate && \
           (cd bot && node index.js &) && \
           gunicorn rentals_backend.wsgi:application --chdir backend --bind 0.0.0.0:8000"

