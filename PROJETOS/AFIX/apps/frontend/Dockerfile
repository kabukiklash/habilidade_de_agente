FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
COPY packages/shared packages/shared
COPY apps/frontend apps/frontend

RUN npm ci
RUN npm run build -w @afix/shared
RUN npm run build -w @afix/frontend

FROM nginx:alpine
COPY --from=builder /app/apps/frontend/dist /usr/share/nginx/html
COPY apps/frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
