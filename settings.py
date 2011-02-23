# Django settings for w91011 project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os
HERE = os.path.normpath(os.path.dirname(__file__))

EMAIL_HOST = 'mail.fry-it.com'
EMAIL_SUBJECT_PREFIX = '[W91011] '

ADMINS = (
     ('Peter Bengtsson', 'peter@fry-it.com'),
)
WEBMASTER_EMAIL = 'ashleynoval@gmail.com'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'w91011',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(HERE, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'


# Make this unique, and don't share it with anybody.
SECRET_KEY = ')z@&sl3r@qu7q=gh7xlgr8hl8%0!1+#zgtgiy-a*xt@@(8qpbo'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(HERE, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'rsvp',
    'website',
)

MIGRATIONS_ROOT = os.path.join(HERE, 'migrations')
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
LOG_FILENAME = os.path.join(HERE, 'event.log')

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'website.middleware.InvitationKeysMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.contrib.messages.context_processors.messages',
    "context_processors.context",
)


INVITATION_KEYS = (
  'ashleyisalittlecutefish',
)

LOGIN_URL = '/login/'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 300

PROJECT_NAME = "Ashley and Peter's wedding 2011"

try:
    from local_settings import *
except ImportError:
    pass

import logging
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    format="%(asctime)s %(levelname)s %(name)s %(message)s",
                   )
