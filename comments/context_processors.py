from django.conf import settings

def html_header_content(context):
    return {
        'STATIC_URL': settings.STATIC_URL,
        'MEDIA_URL': settings.MEDIA_URL,
        'IMAGE_URL': settings.IMAGE_URL,
        'THUMBNAIL_URL': settings.THUMBNAIL_URL,
    }