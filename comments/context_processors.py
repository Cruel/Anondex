from django.conf import settings

def html_header_content(context):
    return {
        'HEAD_JS_FILES': settings.HEAD_JS_FILES,
        'HEAD_CSS_FILES': settings.HEAD_CSS_FILES,
        'STATIC_URL': settings.STATIC_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'IMAGE_URL': settings.IMAGE_URL,
        'THUMBNAIL_URL': settings.THUMBNAIL_URL,
    }