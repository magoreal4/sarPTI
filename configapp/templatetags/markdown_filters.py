from django import template
from markdownx.utils import markdownify

register = template.Library()

@register.filter
def markdownify_custom(value):
    return markdownify(value)
