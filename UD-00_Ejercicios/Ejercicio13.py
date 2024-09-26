import random

# Creo la lista vacía, para posteriormente rellenarla
lista = []

for i in range (0, 10):
    # Usamos el random.randint para obtener números aleatorios dentro del rango 1 y 50
    lista.append(random.randint(1, 50))  

num = int(input("Introduce un número que crea que esté en la lista: "))

if num in (lista):
    print("Bingo!!")
else:
    print("Ese número no está en la tabla.")

print("La tabla es:", lista)
