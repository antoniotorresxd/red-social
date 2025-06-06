FROM nginx:stable-alpine

# Remover configuración por defecto
RUN rm /etc/nginx/conf.d/default.conf

# Copiar nuestra configuración
COPY prod.conf /etc/nginx/conf.d/default.conf

# Crear directorio para logs si es necesario
RUN mkdir -p /var/log/nginx

# Exponer puerto 80
EXPOSE 80

# Verificar configuración de nginx antes de iniciar
RUN nginx -t

# Iniciar nginx
CMD ["nginx", "-g", "daemon off;"]