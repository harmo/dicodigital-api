import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SECRET_KEY = os.environ.get(
        'DJANGO_SECRET_KEY',
        '*a8-=b!z34(hv2ak7s(c_guh5*7aq!7z=da=cp&t3gd&ifrl6i'
    )
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = ['*']


# Application definition

DJANGO_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'rest_framework_swagger',
)

PROJECT_APPS = (
    'dicodigital.dico',
)

if 'TRAVIS' not in os.environ:
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'dicodigital.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dicodigital.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}


# Cache
# https://docs.djangoproject.com/en/1.8/ref/settings/#caches
CACHE = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Rest framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
}


# CORS

CORS_ORIGIN_ALLOW_ALL = True


# Logging
if DEBUG:
    try:
        import debug_toolbar  # NOQA
    except ImportError:
        pass
    else:
        INTERNAL_IPS = (
            '127.0.0.1',
        )

        INSTALLED_APPS += (
            'debug_toolbar',
        )

        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        )

        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
            'HIDE_DJANGO_SQL': False,
        }

        DEBUG_TOOLBAR_PANELS = (
            'debug_toolbar.panels.timer.TimerDebugPanel',
            'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
            'debug_toolbar.panels.template.TemplateDebugPanel',
            'debug_toolbar.panels.sql.SQLDebugPanel',
            'debug_toolbar.panels.signals.SignalDebugPanel',
            # 'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
            # 'debug_toolbar.panels.headers.HeaderDebugPanel',
            # 'debug_toolbar.panels.version.VersionDebugPanel',
            # 'debug_toolbar.panels.logger.LoggingPanel',
        )
