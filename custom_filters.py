from django import template

register = template.Library()

def numeros_a_letras(value):
    numeros = {
        '0': 'cero',
        '1': 'uno',
        '2': 'dos',
        '3': 'tres',
        '4': 'cuatro',
        '5': 'cinco',
        '6': 'seis',
        '7': 'siete',
        '8': 'ocho',
        '9': 'nueve',
    }
    letras = ''.join([numeros[char] if char in numeros else char for char in str(value)])
    return letras

register.filter('numeros_a_letras', numeros_a_letras)
