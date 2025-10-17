#FROM node:20-alpine

#WORKDIR /app
#COPY package*.json ./

#RUN npm install --production

#COPY . .

#CMD ["node", "index.js"]

FROM node:18-bullseye

# Chromium + deps for puppeteer (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates chromium \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY bot/package*.json ./
RUN npm ci --production

COPY bot /app

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

EXPOSE 5000

CMD ["node", "index.js"]

