from django import template

register = template.Library()

@register.filter()
def str_contains(value, arg):
    """
    Usage:
    {% if text|contains:"http://" %}
    This is a link.
    {% else %}
    Not a link.
    {% endif %}
    """  
    return arg in "{}".format(value)

@register.filter()
def func_contains(value, arg):
    """
    Usage:
    {% if text|contains:"http://" %}
    This is a link.
    {% else %}
    Not a link.
    {% endif %}
    """  
    return "{}()".format(arg) in "{}".format(value)