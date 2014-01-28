"""
Django settings for dietzcar project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf.global_settings import DATABASES
import dj_database_url
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sj2@d^=#y2(m9d%ax#fx$35r3)-mjk)@)luhd7iy$bze6dqde2'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get('DEBUG', False)
DEBUG = False

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'carshare',
    #'django.contrib.admin',
    'geoposition',
    'jquery',
    'storages'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dietzcar.urls'

WSGI_APPLICATION = 'dietzcar.wsgi.application'

#TEMPLATE_DIRS = ("dietzcar/templates")
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, '../', "templates"),
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = 'carshare/static/'

if DEBUG:
    STATIC_URL = '/static/'
else:
    #STATIC_URL = 'https://s3-eu-west-1.amazonaws.com/dietzcar/static/'
    STATIC_URL = 'https://dietzcar.s3.amazonaws.com/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = 'dietzcar'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_QUERYSTRING_AUTH = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#     # Allow all host headers
ALLOWED_HOSTS = ['*']
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


# Parse database configuration from $DATABASE_URL

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, '../static'),
# )