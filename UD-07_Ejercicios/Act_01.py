import numpy as np

ceros = np.zeros((3, 4))

print("Matríz de ceros: ")
print(ceros)

# Cambiar la primera fila a uno
print("Matríz cambiada con primera fila a unos: ")
ceros[0] = 1
print(ceros)

# Cambiar la última fila a mi último número del DNI
print("Matríz con última fila con mi último número del DNI:")
ceros[2] = 2
print(ceros)

