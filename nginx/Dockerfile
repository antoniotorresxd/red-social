# Imagen base ligera de Nginx
FROM nginx:stable-alpine

# Elimina la configuración por defecto y copia la tuya
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expone el puerto 80
EXPOSE 80

# Arranca nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]
