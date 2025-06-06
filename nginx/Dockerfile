FROM nginx:stable-alpine

# Remover configuración por defecto
RUN rm /etc/nginx/conf.d/default.conf

# Copiar nuestra configuración
COPY prod.conf /etc/nginx/conf.d/default.conf

# Crear directorio para logs y asegurar permisos
RUN mkdir -p /var/log/nginx && \
    chown -R nginx:nginx /var/log/nginx

# Exponer puertos (80 para HTTP, 443 para HTTPS)
EXPOSE 80
EXPOSE 443

# Verificar configuración de nginx antes de iniciar
RUN nginx -t

# Iniciar nginx
CMD ["nginx", "-g", "daemon off;"]