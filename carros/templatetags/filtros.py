from django import template
from datetime import datetime

register = template.Library()

@register.filter
def mostrar_duracao(value1, value2):
    if all((isinstance(value1, datetime), isinstance(value2, datetime))):
        dias = (value1 - value2).days
        texto = 'Dias'
        if dias == 1:
           texto = 'Dia'
        return f"{dias} {texto}"
    
    return "Não foi devolvido."