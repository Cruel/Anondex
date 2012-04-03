from django import template
register = template.Library()

@register.simple_tag
def mediathumb(obj, width):
    return obj.thumbnail(width)

@register.simple_tag(takes_context=True)
def evalformat(context, varname, format_string, *args):
    context[varname] = eval(format_string % args)
    return '' # Just assign the `varname` variable and return nothing

@register.tag(name='eval')
def do_eval(parser, token):
    "Usage: {% eval %}1 + 1{% endeval %}"

    nodelist = parser.parse(('endeval',))

    class EvalNode(template.Node):
        def render(self, context):
            return eval(nodelist.render(context))

    parser.delete_first_token()
    return EvalNode()