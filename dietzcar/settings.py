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

DEBUG = True

TEMPLATE_DEBUG = True

APPEND_SLASH = True

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
    'storages',
    #'userena',
    #'guardian',
    #'easy_thumbnails',
    #'accounts',
    'rest_framework',
    'south',
    'social.apps.django_app.default',
    'sorl',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    #'userena.backends.UserenaAuthenticationBackend',
    #'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'auth_pipelines.pipelines.get_profile_data',  # custom
    'auth_pipelines.pipelines.get_profile_avatar',  # custom
)


ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'carshare.UserProfile'

# LOGIN_URL          = '/login-form/'
# LOGIN_REDIRECT_URL = '/logged-in/'
# LOGIN_ERROR_URL    = '/login-error/'


# SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
# SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'



SOCIAL_AUTH_FACEBOOK_KEY              = '414725015296995'
SOCIAL_AUTH_FACEBOOK_SECRET          = '31d1e1884b2c115fa5db73768c09186c'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'social.apps.django_app.context_processors.backends',
    'django.core.context_processors.request',
    'social.apps.django_app.context_processors.login_redirect',
)

ROOT_URLCONF = 'dietzcar.urls'

WSGI_APPLICATION = 'dietzcar.wsgi.application'

#TEMPLATE_DIRS = ("dietzcar/templates")
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, '../', "templates"),
)

REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
    ),

}

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

MEDIA_ROOT = 'media/'

if DEBUG:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
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