num1 = int(input("Introduce un número: "))
num2 = int(input("Introduce otro número: "))

if num1 > num2:
    print("El número mayor es", num1, "y el menor", num2)
elif num1 < num2:
    print("El número mayor es", num2, "y el menor", num1)
else:
    print("Los números son iguales")
