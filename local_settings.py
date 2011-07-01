
LOGIN_URL          = '/accounts/login/'
LOGIN_REDIRECT_URL = '/socialauth/logged-in/'
LOGIN_ERROR_URL    = '/socialauth/error/'

SOCIAL_AUTH_DEFAULT_USERNAME = 'NewUser'
# If a custom redirect URL is needed that must be different to LOGIN_URL
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/another-login-url/'
# Different URL for newly registered users
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-login-url/'
# This defines the desired session key where last error message should be stored. It's disabled by default.
SOCIAL_AUTH_ERROR_KEY = 'social_errors'

# Final user name will have a random UUID-generated suffix in case it's already taken.
SOCIAL_AUTH_UUID_LENGTH = 6

# Backends will store extra values from response by default, set this to False to avoid such behavior
#SOCIAL_AUTH_EXTRA_DATA = False
# Configure authentication and association complete URL names to avoid possible clashes:
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'associate_complete'

TWITTER_CONSUMER_KEY         = 'lqhF3XvLwo6G3F629u5apA'
TWITTER_CONSUMER_SECRET      = 'TSU4xx8Oc3wlhD5pxuLA2tCGS2X3jZ7jmG8JwU3Z3M'
FACEBOOK_APP_ID              = '156994677702749'
FACEBOOK_API_SECRET          = 'bef3c281976a10bdd0d6ff7683c423be'
LINKEDIN_CONSUMER_KEY        = ''
LINKEDIN_CONSUMER_SECRET     = ''
ORKUT_CONSUMER_KEY           = '555779437648'
ORKUT_CONSUMER_SECRET        = 'XFmDOokC9oguQfrrjv32tXbf'
GOOGLE_CONSUMER_KEY          = 'anondex.com'
GOOGLE_CONSUMER_SECRET       = 'aCJWoaSaE_fldzIkUl60w7MP'
GOOGLE_DISPLAY_NAME          = 'Anondex'
GOOGLE_OAUTH2_CLIENT_KEY     = 'AIzaSyCUMKqhtCcJwahh4a4Robw600R_s_jQweM'
GOOGLE_OAUTH2_CLIENT_SECRET  = 'XeYMV_E02MgHXlhrrfozVkZ7'
FOURSQUARE_CONSUMER_KEY      = ''
FOURSQUARE_CONSUMER_SECRET   = ''

# Custom backends
SOCIAL_AUTH_IMPORT_BACKENDS = (
    #'myproy.social_auth_extra_services',
)

ACCOUNT_ACTIVATION_DAYS = 7

AUTH_PROFILE_MODULE = 'socialauth.Profile'
#SOCIAL_AUTH_USER_MODEL = 'socialauth.CustomUser'

HEAD_JS_FILES = {
    'swfupload/swfupload',
    'jquery.swfupload',
    'jquery.fancybox-1.3.4',
    'jquery.jmc_resizr',
    'jquery.taghandler',
    'jquery.cluetip',
    'jquery.hoverIntent',
    'create2',
    'comments',
    'main',
    'report',
    'flashplayer',
}

HEAD_CSS_FILES = {
    'index',
    'imprimis',
    'browse',
    'comments',
    'create',
    'framer',
    'hoverdiv',
    'report',
    'stars',
    'jquery.fancybox-1.3.4',
    'jquery-ui-1.8.9.custom',
    'jquery.cluetip',
    'data',
    'layout',
}