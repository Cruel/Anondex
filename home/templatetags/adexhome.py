from django import template
register = template.Library()

@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>
  """
  return range(1, value+1)

@register.simple_tag
def rating_style( value, size=False ):
    new_size = '18px'
    extra = ''
    if value == 0:
        color = '#000'
        new_size = '16px'
        extra = 'text-shadow:none;'
    elif 1 <= value <= 2:
        color = 'red'
    elif 2 < value < 3:
        color = '#000'
        new_size = '20px'
    elif 3 <= value < 4:
        color = '#5D5'
        new_size = '24px'
    else:
        color = '#0D0'
        new_size = '28px'

    if size:
        return 'color:%s;font-size:%s;%s' % (color, new_size, extra)
    else:
        return 'color:%s;%s' % (color, extra)