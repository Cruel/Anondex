from django.conf import settings

def auth_context(context):
    return {
        'LOGIN_REDIRECT_URL': settings.LOGIN_REDIRECT_URL,
    }