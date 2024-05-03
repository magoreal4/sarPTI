#!/bin/bash

echo "Creando backup de la base de datos..."

sudo docker-compose exec sar-django python manage.py dumpdata main.empresa --indent 2 > 01_empresa.json
sudo docker-compose exec sar-django python manage.py dumpdata auth.user auth.group main.userprofile --indent 2 > 02_usuarios.json
sudo docker-compose exec sar-django python manage.py dumpdata main.sitio --indent 2 > 03_sitios.json
sudo docker-compose exec sar-django python manage.py dumpdata main.candidato --indent 2 > 04_candidatos.json
sudo docker-compose exec sar-django python manage.py dumpdata registros --indent 2 > 05_registroscampo.json
sudo docker-compose exec sar-django python manage.py dumpdata regostrosgab --indent 2 > 06_registrosgab.json

echo "Archivos creados"
