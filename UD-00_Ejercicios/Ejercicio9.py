def areaRect(lado, ancho):
    return lado * ancho

lado = float(input("Introduce el lado del rectángulo: "))
ancho = float(input("Introduce el ancho del rectángulo: "))
print("El área del rectángulo es: ", areaRect(lado, ancho))
