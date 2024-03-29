THUMBNAIL_URL = 'http://anondex.com/media/i/thumb/'
IMAGE_URL = 'http://anondex.com/media/i/'

# Interval limitation
INTERVAL_ANON_ADEX = 1500
INTERVAL_USER_ADEX = 1500
INTERVAL_ANON_COMMENT = 60
INTERVAL_USER_COMMENT = 20

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/home/me'
LOGIN_ERROR_URL    = '/auth/error/'

SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False

SOCIAL_AUTH_DEFAULT_USERNAME = 'NewUser'
# If a custom redirect URL is needed that must be different to LOGIN_URL
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/auth_redirect/'
# Different URL for newly registered users
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/welcome/'
# URL for newly registered users w/o username set
LOGIN_USERNAME_URL = '/auth/username/'
# This defines the desired session key where last error message should be stored. It's disabled by default.
SOCIAL_AUTH_ERROR_KEY = 'social_errors'

# Final user name will have a random UUID-generated suffix in case it's already taken.
SOCIAL_AUTH_UUID_LENGTH = 3

# Backends will store extra values from response by default, set this to False to avoid such behavior
#SOCIAL_AUTH_EXTRA_DATA = False
# Configure authentication and association complete URL names to avoid possible clashes:
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

# Custom backends
SOCIAL_AUTH_IMPORT_BACKENDS = (
    #'myproy.social_auth_extra_services',
)

ACCOUNT_ACTIVATION_DAYS = 7

AUTH_PROFILE_MODULE = 'socialauth.Profile'
#SOCIAL_AUTH_USER_MODEL = 'socialauth.CustomUser'

SASS_FRAMEWORKS = (
    'compass',
    #'blueprint',
)

MEDIA_BUNDLES = (
    ('anondex.css',
        'css/global.sass',
        'css/browse.sass',
        'css/code.css',
        'css/comments.sass',
        'css/create.sass',
        #'css/data.sass',
        'css/framer.sass',
        'css/hoverdiv.sass',
        'css/home.sass',
        'css/index.sass',
        'css/jquery.cluetip.css',
        'css/jquery.fancybox-1.3.4.css',
        'css/jquery-ui-1.8.9.custom.css',
        'css/layout.sass',
        'css/report.sass',
        'css/stars.sass',
        'css/login.sass',
        'css/medialibrary.sass',
        'css/profile.sass',
    ),
    ('anondex.js',
        'js/jquery.cookies.2.2.0.js',
        'js/jquery.fileupload.js',
        'js/jquery.fancybox-1.3.4.js',
        'js/jquery.jmc_resizr.js',
        'js/jquery.taghandler.js',
        'js/jquery.cluetip.js',
        'js/jquery.hoverIntent.js',
        'js/jquery.scrollto.js',
        'js/jquery.blockUI.js',
        'js/main.js',
        'js/home.js',
        'js/create.js',
        'js/comments.js',
        'js/report.js',
        'js/flashplayer.js',
        'js/medialibrary.js',
        'js/google.analytics.js',
    ),
)

# django-ratings Setting
RATINGS_VOTES_PER_IP = 4


# django-hitcount Settings
HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 1 }
HITCOUNT_HITS_PER_IP_LIMIT = 0
#HITCOUNT_EXCLUDE_USER_GROUP = ( 'Editor', )

from api_keys import *