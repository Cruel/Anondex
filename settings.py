from os.path import abspath, dirname, basename, join
import time

DEBUG = True
PRODUCTION = False
TEMPLATE_DEBUG = DEBUG
MEDIA_DEV_MODE = False

#VERSION = '2.0.0'

INTERNAL_IPS = ('127.0.0.1',)

ROOT_PATH = abspath(dirname(__file__))
PROJECT_NAME = basename(ROOT_PATH)

ADMINS = (
    ('Thomas', 'machin3@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'anondex',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

ROOT_URLCONF = 'urls'

DEV_MEDIA_URL = '/devstatic/'
PRODUCTION_MEDIA_URL = '/static/'

GLOBAL_MEDIA_DIRS = (
    join(ROOT_PATH, 'static'),
    join(ROOT_PATH, '../imported-sass-frameworks'),
)

MEDIA_ROOT = join(ROOT_PATH, '../media/')
STATIC_ROOT = join(ROOT_PATH, 'static/')
if not PRODUCTION:
    MEDIA_URL = 'http://localhost/media/'
    ADMIN_MEDIA_PREFIX = 'http://localhost/media/admin/'
    STATIC_URL = 'http://localhost:8000/static/'
else:
    MEDIA_URL = 'http://anondex.com/media/'
    ADMIN_MEDIA_PREFIX = 'http://anondex.com/media/admin/'
    STATIC_URL = 'http://anondex.com/static/'

YUICOMPRESSOR_PATH = join(ROOT_PATH, '../yuicompressor.jar')
CLOSURE_COMPILER_PATH = join(ROOT_PATH, '../closure.jar')

ROOT_MEDIA_FILTERS = {
    'js': 'mediagenerator.filters.closure.Closure',
    'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
}

FILE_UPLOAD_HANDLERS = (
    #"comments.uploadprogresscachedhandler.UploadProgressCachedHandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    join(ROOT_PATH, 'static'),
)

# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'ib8lfpj-f=sg(!vlqzb@bd)-g+5^d!pp(j_#8gx54iiyp#de9u'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'comments.context_processors.html_header_content',
    'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_type_backends',
    'socialauth.context_processors.auth_context',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    #'social_auth.backends.contrib.LiveJournalBackend',
    #'social_auth.backends.contrib.orkut.OrkutBackend',
    #'social_auth.backends.contrib.foursquare.FoursquareBackend',
    #'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'mediagenerator.middleware.MediaMiddleware', # Media middleware has to come first
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    #'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    #'djangotoolbox',
    'debug_toolbar',
    'mediagenerator',
    'registration',
    'profiles',
    'social_auth',
    'tagging',
    'djangoratings',
    #'djcelery',
    'hitcount',
    'south',
    #'tracking',
    # Anondex Specific

    'home',
    'comments',
    'socialauth',
    'reporting',
    'adex',
    'medialibrary',
    'adextagging',
)

COMMENTS_APP = 'comments'
COMMENT_MAX_LENGTH = 1000

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

import djcelery
djcelery.setup_loader()

from local_settings import *