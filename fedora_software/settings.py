# ~*~ coding: utf-8 ~*~
"""
Django settings for fedora_software project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG   = os.environ.get('DEBUG', False) and True or False
DBDEBUG = os.environ.get('DEBUG', False) == 'DB'
TEMPLATE_DEBUG = os.environ.get('DEBUG', False) == 'TEMPLATE'

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) if DEBUG else '/var/lib/fedora-software'

# SECURITY WARNING: keep the secret key used in production secret!
try:
    with open(os.path.join(BASE_DIR, 'data', 'secret_key')) as f:
        SECRET_KEY = f.read()
except IOError:
    with open(os.path.join(BASE_DIR, 'data', 'secret_key'), 'w') as f:
        from django.utils.crypto import get_random_string
        SECRET_KEY = get_random_string(50,
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
        f.write(SECRET_KEY)

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Jakub Dorňák', 'jdornak@redhat.com'),
    ('Jozef Mlích',  'jmlich@redhat.com'),
)
SERVER_EMAIL = '"Fedora Software" <no-reply@redhat.com>'

# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fedora_software',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'fedora_software.urls'

WSGI_APPLICATION = 'fedora_software.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'htdocs', 'media')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'mail_admins'],
            'level': DEBUG and 'DEBUG' or 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'level': DBDEBUG and 'DEBUG' or 'INFO',
            'propagate': True,
        },
    },
}

AUTHENTICATION_BACKENDS = (
    'fas.backend.FasBackend',
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

FS_HIGHLIGHT_APPS = [
    'shotwell.desktop',
    'datovka.desktop',
    'gimp.desktop',
    'geary.desktop',
    'audacity.desktop',
    'gajim.desktop',
    'firefox.desktop',
    'org.gnome.Weather.Application.desktop',
    'meld.desktop',
    'scratch.desktop',
    'anjuta.desktop',
    'mozilla-thunderbird.desktop',
    'gtkwave.desktop',
    'owncloud.desktop',
    'stellarium.desktop',
    'frozen-bubble.desktop',
    'wesnoth.desktop',
    'scorched3d.desktop',
    'rosegarden.desktop',
    'darktable.desktop',
    'virt-manager.desktop',
    'subsurface.desktop',
    'pitivi.desktop',
]

FS_HIGHLIGHT_CATS = [
    'game',
    'system',
    'utility',
    'audio-video',
    'development',
    'office',
    'education',
    'network',
    'graphics',
    'accessibility',
    'ide',
    'languages',
    'web-browser',
    'finance',
    'chat',
]


FS_SMALL_THUMBNAIL_WIDTH    = 112
FS_SMALL_THUMBNAIL_HEIGHT   = 63
FS_MEDIUM_THUMBNAIL_WIDTH   = 624
FS_MEDIUM_THUMBNAIL_HEIGHT  = 351
FS_LARGE_THUMBNAIL_WIDTH    = 752
FS_LARGE_THUMBNAIL_HEIGHT   = 423

