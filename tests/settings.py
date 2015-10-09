import warnings
from dicodigital.settings import *  # NOQA

warnings.simplefilter('always')

DEBUG = False

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_ci_test',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

INSTALLED_APPS += (
    'tests',
)
