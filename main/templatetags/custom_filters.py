from django import template

register = template.Library()

@register.filter
def split(value, separator=','):
    """Split a string by separator and return list"""
    if not value:
        return []
    return [item.strip() for item in value.split(separator) if item.strip()]