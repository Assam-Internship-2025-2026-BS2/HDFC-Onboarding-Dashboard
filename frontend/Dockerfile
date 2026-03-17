# -------- Stage 1: Build React App --------
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build


# -------- Stage 2: Serve with Nginx --------
FROM nginx:1.25-alpine

# Copy custom nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# remove default nginx html
RUN rm -rf /usr/share/nginx/html/*

# copy build files (Vite outputs to dist/)
COPY --from=builder /app/dist /usr/share/nginx/html

# DS-0002: run as non-root user
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid
USER nginx

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]