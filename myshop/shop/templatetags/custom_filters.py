from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """Comprueba si una cadena comienza con un prefijo específico."""
    return value.startswith(arg)