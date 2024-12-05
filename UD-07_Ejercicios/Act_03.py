import numpy as np

array = np.random.randint(1, 101, 10) # Rango hasta 101 para que incluya el 100

print("Array de números aleatorios: ")
print(array)

print("Array con valores mayores a 50: ")
print(array[array > 50])

