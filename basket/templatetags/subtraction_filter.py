from django import template


register = template.Library()


# Basic subtraction filter
@register.filter(name='subtract')
def subtract(a, b):
    return a - b
