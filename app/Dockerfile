FROM node:15 as builder

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY . .
RUN npm run build

FROM caddy:2 
COPY --from=builder /app/dist/ /srv
COPY --from=builder /app/Caddyfile /etc/caddy/Caddyfile
EXPOSE 8080
