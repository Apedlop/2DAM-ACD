import transaction
from ZODB import FileStorage, DB

# Definición de la clase Movil
class Movil:
    def __init__(self, marca, modelo, anio_lanzamiento, sistema_operativo):
        self.marca = marca
        self.modelo = modelo
        self.anio_lanzamiento = anio_lanzamiento
        self.sistema_operativo = sistema_operativo

# Configuración de la base de datos
storage = FileStorage.FileStorage('moviles.fs')
db = DB(storage)
connection = db.open()
root = connection.root

# Inicializa la raíz si está vacía
if not hasattr(root, 'moviles'):
    root.moviles = {}

# Almacenar varios objetos Movil
def almacenar_moviles():
    movil1 = Movil("Apple", "iPhone 14", 2022, "iOS")
    movil2 = Movil("Samsung", "Galaxy S22", 2022, "Android")
    movil3 = Movil("Xiaomi", "Redmi Note 11", 2022, "Android")

    # Almacenar los móviles en la base de datos
    root.moviles['movil1'] = movil1
    root.moviles['movil2'] = movil2
    root.moviles['movil3'] = movil3

    # Confirmar los cambios
    transaction.commit()

# Consultar objetos Movil
def consultar_moviles(sistema_operativo_filtro):
    print(f"Moviles con sistema operativo {sistema_operativo_filtro}:")
    for key in root.moviles.keys():
        movil = root.moviles[key]
        # Verifica si el objeto tiene el atributo 'sistema_operativo' y filtra
        if hasattr(movil, 'sistema_operativo') and movil.sistema_operativo == sistema_operativo_filtro:
            print(f"Marca: {movil.marca}, Modelo: {movil.modelo}, Año: {movil.anio_lanzamiento}, SO: {movil.sistema_operativo}")

# Función principal
def main():
    almacenar_moviles()
    consultar_moviles("Android")  # Cambia "Android" por "iOS" si deseas consultar los móviles de Apple

# Ejecuta el programa
if __name__ == "__main__":
    main()

    # Cierra la conexión
    connection.close()
    db.close()