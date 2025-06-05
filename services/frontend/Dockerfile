# Etapa 1: Build del frontend
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Etapa 2: Servir con Nginx (imagen oficial)
FROM nginx:alpine

# Elimina la configuración por default de nginx (opcional)
RUN rm -rf /usr/share/nginx/html/*

# Copia la app compilada
COPY --from=build /app/dist /usr/share/nginx/html

# Opcional: copia tu nginx.conf custom si lo tienes
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
