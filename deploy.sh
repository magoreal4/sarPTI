#!/bin/bash
# -*- ENCODING: UTF-8 -*-

read -p "Nombre de la App: " app
read -p "Dominio: " dominio
read -p "Puerto: " puerto
cat > ${app} <<EOF
# /etc/nginx/sites-available/$app

upstream web_$app {
    server localhost:$puerto;
}
server {
    server_name $dominio www.${dominio};

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
        }

    location /static/ {
        autoindex on;
        alias $PWD/staticfiles/;
        }
    
    location /media/ {
        autoindex on;
        alias $PWD/media/;
        }

    location / {
        proxy_pass http://web_$app;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_redirect off;    
        }
}
EOF

cat > docker-compose.yml <<EOF
version: "3.9"

services:

  django:
    container_name: $app-Django
    build: .
    restart: always
    ports:
    - $puerto:8000
    volumes:
    - ./:/app
    depends_on:
      - db

  db:
    image: postgres:14.3-alpine3.16
    container_name: $app-db
    ports:
      - 5433:5432
    environment:
      - POSTGRES_DB=base
      - POSTGRES_USER=magoreal
      - POSTGRES_PASSWORD=ojalaque
    volumes:
      - ./db:/var/lib/postgresql/data
EOF

sudo mv .env.sample .env

sudo docker-compose up -d --build

sudo cp $app /etc/nginx/sites-available/$app
sudo ln -s /etc/nginx/sites-available/$app /etc/nginx/sites-enabled/$app
nginx -t




exit