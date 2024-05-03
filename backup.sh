#!/bin/bash

echo "Creando backup de la base de datos..."

sudo docker-compose exec sar-django python manage.py dumpdata main.empresa --indent 2 > 01_empresa.json --settings=config.settings.prod
echo "Base de empresa creada..."

sudo docker-compose exec sar-django python manage.py dumpdata auth.user auth.group main.userprofile --indent 2 > 02_usuarios.json --settings=config.settings.prod
echo "Base de usuarios creada..."

sudo docker-compose exec sar-django python manage.py dumpdata main.sitio --indent 2 > 03_sitios.json --settings=config.settings.prod
echo "Base de datos sitios creada..."

sudo docker-compose exec sar-django python manage.py dumpdata registros --indent 2 > 04_registroscampo.json --settings=config.settings.prod
echo "Base de registros de campo creada..."

sudo docker-compose exec sar-django python manage.py dumpdata registrosgab --indent 2 > 05_registrosgab.json --settings=config.settings.prod
echo "Base de registros de gabinete creada..."

echo "Archivos creados"
