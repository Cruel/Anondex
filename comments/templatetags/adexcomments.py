from django import template
from comments.utils import get_fancy_time
register = template.Library()

@register.filter
def timeago(value):
    return get_fancy_time(value)