from django import template


register = template.Library()


# Basic subtraction filter.
# Requires:
#   a: Number
#   b: Number to subtract from a
@register.filter(name='subtract')
def subtract(a, b):
    return a - b
