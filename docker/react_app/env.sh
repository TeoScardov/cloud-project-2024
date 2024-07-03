#!/bin/sh

# Crea il file di configurazione runtime
echo "window._env_ = {" > /usr/share/nginx/html/env-config.js

# Itera su tutte le variabili d'ambiente
env | while IFS='=' read -r key value
do
    # Controlla se la chiave inizia con VITE_
    case $key in
        VITE_*)
            # Escapa eventuali caratteri speciali nel valore
            escaped_value=$(printf '%s\n' "$value" | sed -e 's/[\/&]/\\&/g')
            echo "  $key: \"$escaped_value\"," >> /usr/share/nginx/html/env-config.js
            ;;
    esac
done

echo "};" >> /usr/share/nginx/html/env-config.js

# Esegui nginx
exec "$@"