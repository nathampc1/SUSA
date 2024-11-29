from django import template
import re

register = template.Library()

@register.filter
def format_cnpj(value):
    # Remove caracteres não numéricos
    return re.sub(r'\D', '', value)
