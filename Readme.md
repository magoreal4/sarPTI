# Dj-skeleton

```shell
python3 -m venv .venv
source .venv/bin/activate
```

```
pip install django
django-admin startproject config .

```

```
docker exec -it postgres psql -U magoreal -d base
python manage.py runserver --settings=config.settings.prod

python manage.py collectstatic --no-input --settings=config.settings.prod
python manage.py migrate --settings=config.settings.prod
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```


sudo apt-get install -y jq

sudo docker-compose exec sar-django python manage.py makemigrations --settings=config.settings.prod
sudo docker-compose exec sar-django python manage.py migrate --settings=config.settings.prod

sudo docker-compose exec sar-django rm -r db

sudo docker-compose exec sar-django python manage.py createsuperuser --settings=config.settings.prod
