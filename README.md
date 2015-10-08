# DicoDigital API

API for [https://lite6.framapad.org/p/dicodigital](https://lite6.framapad.org/p/dicodigital)

Build with [Django](https://www.djangoproject.com/) and [Django-rest-framework](http://www.django-rest-framework.org/)

## Requirements

* Python 3
* Virtualenv

## Development

Get the project and install dependencies:

```bash
git clone https://github.com/harmo/dicodigital-api.git
cd dicodigital-api
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
```

Set environement variables:

→ [dj-database-url](https://github.com/kennethreitz/dj-database-url#url-schema)

```bash
export DJANGO_SETTINGS_MODULE=dicodigital.settings
export DATABASE_URL=sqlite:///$(pwd)/dicodigital.db
export DEBUG=True
```

Migrate the database:

```bash
./manage.py migrate
```

This step allow you to create a superadmin user:

```bash
./manage.py createsuperuser
```

Run the magic:

```bash
./manage.py runserver_plus
```
