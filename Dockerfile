# ===============================
# Stage 1: Node.js bot build
# ===============================
FROM node:18-bullseye AS nodebot

WORKDIR /bot

COPY bot/package*.json ./
RUN npm install --omit=dev
COPY bot/ .

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# ===============================
# Stage 2: Django backend
# ===============================
FROM python:3.11-slim

# Create working directory
WORKDIR /app

# Copy backend code
COPY backend /app/backend
COPY backend/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy bot from Node build
COPY --from=nodebot /bot /app/bot

# Expose port for Railway
EXPOSE 8000

# Command to start both Django and the bot
CMD sh -c "cd /app/backend && python manage.py migrate && \
            (cd /app/bot && node index.js &) && \
            gunicorn rentals_backend.wsgi:application --bind 0.0.0.0:8000"

