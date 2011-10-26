from django import template
register = template.Library()

@register.simple_tag
def mediathumb(obj, width):
    return obj.thumbnail(width)