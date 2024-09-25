def mayor(num1, num2):
    if num1 < num2:
        return num2
    else:
        return num1

num1 = int(input("Introduce un número: "))
num2 = int(input("Introduce otro número: "))
print("El número mayor es:", mayor(num1, num2))
