# Django settings for squidweb project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Michael Axiak', 'axiak@mit.edu',)
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(ROOT, 'sqldb.db')

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

MEDIA_ROOT = os.path.join(ROOT, 'public_html', 'media')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin'

SECRET_KEY = '9&2zer8b!x*l1silqvk!n4e49xczbj&x$)n_ds_@!o+0+^+2=m'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'squidweb.urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'squidweb.squid',
)

TEMPLATE_CONTEXT_PROCESSORS = ('squidweb.context_processors.media_url',)

URL_ROOT = '/'

try:
    from site_settings import *
except ImportError:
    pass
