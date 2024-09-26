import random

# Creamos una lista vacía para rellenarla proximamente
lista = []

for i in range (1, 11):
    # Usamos el random.randint para obtener números aleatorios dentro del rango 1 y 50
    lista.append(random.randint(1, 50))  

print(lista)
