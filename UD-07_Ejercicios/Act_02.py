import numpy as np

aleatorios = np.random.randint(1, 10, (4, 4)) # Rasgo hasta 10 para que se incluya el 9

print("Matríz de números aleatorios: ")
print(aleatorios)

print("Matríz con diagonal cambiada al primer número de mi DNI:")
np.fill_diagonal(aleatorios, 2)
print(aleatorios)

