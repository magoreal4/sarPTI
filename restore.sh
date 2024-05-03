#!/bin/bash

echo "Recuperando backup de la base de datos..."

python manage.py loaddata 01_empresa.json
echo "Base de empresa recuperada..."

python manage.py loaddata 02_usuarios.json
echo "Base de usuarios recuperada..."

python manage.py loaddata 03_sitios.json
echo "Base de sitios recuperada..."

python manage.py loaddata 04_registroscampo.json
echo "Base de registros de campo recuperada..."

python manage.py loaddata 05_registrosgab.json
echo "Base de registros de gabinete recuperada..."
