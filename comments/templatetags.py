from django import template
register = template.Library()

@register.filter
def to_currency(value, arg):
    return ((value/5)*100)-1