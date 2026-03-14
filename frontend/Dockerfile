# ─────────────────────────────────────────────────────────
# PriceIntel — Frontend Dockerfile
# Multi-stage: build with Node, serve with nginx
# ─────────────────────────────────────────────────────────

# ── Stage 1: Build ───────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for Docker layer caching
COPY package*.json ./
RUN npm ci --frozen-lockfile

# Copy source and build
COPY . .

# VITE_API_BASE_URL will be injected at build time via --build-arg
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# ── Stage 2: Serve with nginx ─────────────────────────────
FROM nginx:1.25-alpine AS runtime

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config for serving the SPA
COPY nginx-frontend.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Ensure proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
