import re
from django import template
register = template.Library()

@register.filter
def flatpage_title(title):
    return re.sub('^\d+\.?\s*', '', title)
