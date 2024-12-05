import numpy as np

array = np.random.randint(0, 51, 20)

# Reestructurar el array en una matriz de 4 x 5
matriz = array.reshape(4, 5)

# Calcular la suma de cada columna
sumaColum = np.sum(matriz, axis = 0)

print("Matríz de 4 x 5:")
print(matriz)

print("Suma de las columnas de la matríz: ")
print(sumaColum)

