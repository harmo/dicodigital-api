import warnings
from dicodigital.settings import *  # NOQA

warnings.simplefilter('always')

DEBUG = False

INSTALLED_APPS += (
    'tests',
)