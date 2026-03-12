FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
COPY packages/shared packages/shared
COPY apps/backend apps/backend

RUN npm ci
RUN npm run build -w @afix/shared
RUN npm run build -w @afix/backend

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/apps/backend/dist ./dist
COPY --from=builder /app/apps/backend/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

ENV NODE_ENV=production
EXPOSE 3002
CMD ["node", "dist/main.js"]
