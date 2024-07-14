# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='range_filter')
def range_filter(value):
    return range(value)
