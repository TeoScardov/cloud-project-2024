# FROM --platform=linux/amd64 node:18-alpine as build

# WORKDIR /app

# # COPY package.json package-lock.json ./
# #RUN npm ci
# COPY package.json ./
# RUN npm install

# COPY . .
# RUN npm run build

# # Serve stage
# FROM --platform=linux/amd64 nginx:alpine

# COPY --from=build /app/dist /usr/share/nginx/html
# COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# COPY env.sh /docker-entrypoint.d/40-env.sh
# RUN chmod +x /docker-entrypoint.d/40-env.sh

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
FROM --platform=linux/amd64 node:18-alpine as build

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

# Serve stage
FROM --platform=linux/amd64 nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copia lo script env.sh
COPY env.sh /env.sh
RUN chmod +x /env.sh

EXPOSE 80

# Usa env.sh come entrypoint
ENTRYPOINT ["/env.sh"]
CMD ["nginx", "-g", "daemon off;"]


