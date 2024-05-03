#!/bin/bash

echo "Recuperando backup de la base de datos..."

sudo python manage.py dumpdata 01_empresa.json
echo "Base de empresa recuperada..."

sudo python manage.py dumpdata 02_usuarios.json
echo "Base de usuarios recuperada..."

sudo python manage.py dumpdata 03_sitios.json
echo "Base de sitios recuperada..."

sudo python manage.py dumpdata 04_registroscampo.json
echo "Base de registros de campo recuperada..."

sudo python manage.py dumpdata 05_registrosgab.json
echo "Base de registros de gabinete recuperada..."
