# Test, deploy !!

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# DicoDigital API

API for [https://lite6.framapad.org/p/dicodigital](https://lite6.framapad.org/p/dicodigital)

Build with [Django](https://www.djangoproject.com/) and [Django-rest-framework](http://www.django-rest-framework.org/)


## Requirements

* Python 3
* Virtualenv


## Install

Create a virtualenv, then source in
```bash
$ virtualenv [env]
$ source env/bin/activate
```

Install requirements
```bash
$ pip install -r requirements/dev.txt
```

Set environement variables

→ [dj-database-url](https://github.com/kennethreitz/dj-database-url#url-schema)
```bash
$ export DJANGO_SETTINGS_MODULE=dicodigital.settings
$ export DATABASE_URL=[dj-database-url]
$ export DEBUG=[True/False]
```

Migrate the database

This step allow you to create a superadmin user
```bash
$ django-admin.py migrate
```

Run the magic
```bash
$ django-admin.py runserver_plus
```