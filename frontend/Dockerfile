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

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]