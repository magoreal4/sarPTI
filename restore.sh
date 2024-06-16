#!/bin/bash

echo "Recuperando backup de la base de datos..."

python manage.py loaddata 01_empresa.json
echo "Base de empresa recuperada..."

python manage.py loaddata 02_groups.json
echo "Base de usuarios recuperada..."

python manage.py loaddata 03_permisos.json
echo "Base de sitios recuperada..."

python manage.py loaddata 04_usuarios.json
echo "Base de registros de campo recuperada..."

python manage.py loaddata 05_sitios.json
echo "Base de registros de gabinete recuperada..."

python manage.py loaddata 06_registroscampo.json
echo "Base de registros de Politicas recuperada..."

python manage.py loaddata 07_registrosgab.json
echo "Base de registros de Terminos recuperada..."