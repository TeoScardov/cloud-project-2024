#!/bin/sh

# Sostituisci le variabili d'ambiente in env.js
sed -i "s|\${VITE_ACCOUNT_SERVICE_URL}|$VITE_ACCOUNT_SERVICE_URL|g" /usr/share/nginx/html/env.js
sed -i "s|\${VITE_PURCHASE_SERVICE_URL}|$VITE_PURCHASE_SERVICE_URL|g" /usr/share/nginx/html/env.js
sed -i "s|\${VITE_PRODUCT_CATALOG_URL}|$VITE_PRODUCT_CATALOG_URL|g" /usr/share/nginx/html/env.js
sed -i "s|\${VITE_SHOPPING_CART_URL}|$VITE_SHOPPING_CART_URL|g" /usr/share/nginx/html/env.js
sed -i "s|\${VITE_NUMBER_OF_BOOKS_TO_DISPLAY}|$VITE_NUMBER_OF_BOOKS_TO_DISPLAY|g" /usr/share/nginx/html/env.js

# Esegui il comando originale
exec "$@"