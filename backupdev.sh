#!/bin/bash

echo "Creando backup de la base de datos..."

python manage.py dumpdata main.empresa --indent 2 > 01_empresa.json 
echo "Base de empresa creada..."

python manage.py dumpdata auth.user auth.group main.userprofile --indent 2 > 02_usuarios.json 
echo "Base de usuarios creada..."

python manage.py dumpdata main.sitio --indent 2 > 03_sitios.json 
echo "Base de datos sitios creada..."

python manage.py dumpdata registros --indent 2 > 04_registroscampo.json 
echo "Base de registros de campo creada..."

python manage.py dumpdata registrosgab --indent 2 > 05_registrosgab.json 
echo "Base de registros de gabinete creada..."

echo "Archivos creados"
