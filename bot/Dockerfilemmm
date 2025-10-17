#FROM node:20-alpine

#WORKDIR /app
#COPY package*.json ./

#RUN npm install --production

#COPY . .

#CMD ["node", "index.js"]

FROM node:18-bullseye

# chromium deps for puppeteer
RUN apt-get update && apt-get install -y --no-install-recommends chromium && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

EXPOSE 5000
CMD ["node", "index.js"]

