FROM image-registry.openshift-image-registry.svc:5000/06dc2b-prod/node:15 as builder

WORKDIR /app

COPY package*.json /app/

RUN npm ci

COPY . .
RUN npm run build

FROM image-registry.openshift-image-registry.svc:5000/06dc2b-prod/caddy:2 
COPY --from=builder /app/dist/ /srv
COPY --from=builder /app/Caddyfile /etc/caddy/Caddyfile
EXPOSE 8080
