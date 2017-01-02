# DicoDigital API  [![dicodigital-api on Travis](https://travis-ci.org/harmo/dicodigital-api.svg?branch=master)](https://travis-ci.org/harmo/dicodigital-api)

API for [https://lite6.framapad.org/p/dicodigital](https://lite6.framapad.org/p/dicodigital)

Build with [Django](https://www.djangoproject.com/) and [Django-rest-framework](http://www.django-rest-framework.org/)

# One click deploy !!

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


## Requirements

* Docker
* Docker-compose


## Development

Get the project and install dependencies:

```bash
git clone https://github.com/harmo/dicodigital-api.git
cd dicodigital-api
```

Set environement variables in .env file:

```bash
export DATABASE_URL=sqlite:///$(pwd)/dicodigital.db
```
→ [dj-database-url](https://github.com/kennethreitz/dj-database-url#url-schema)

Run the magic:

```bash
make install up
```


## API Documentation

[Django REST Swagger](https://github.com/marcgibbons/django-rest-swagger/) was installed and is accessible directly from your app to ```/docs/```