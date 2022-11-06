from xmlrpc.client import Boolean
from django import template

register = template.Library()

@register.filter()
def startswith(string, val) -> bool:
    return string.startswith(val)