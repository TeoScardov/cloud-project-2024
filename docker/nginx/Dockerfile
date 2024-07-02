# Usa l'immagine base di Nginx
FROM nginx:latest

# Copia il file di configurazione di Nginx nel container
COPY nginx.conf /etc/nginx/nginx.conf

# Esponi la porta 4000 per Nginx
EXPOSE 4000

# Comando di avvio predefinito di Nginx
CMD ["nginx", "-g", "daemon off;"]
