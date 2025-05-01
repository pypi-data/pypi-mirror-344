import random

def sortear_numero(inicio, fim):
    """
    Função que sorteia um número entre o intervalo [inicio, fim].
    """
    return random.randint(inicio, fim)

def sortear_item(lista):
    """
    Função que sorteia um item de uma lista.
    """
    return random.choice(lista)