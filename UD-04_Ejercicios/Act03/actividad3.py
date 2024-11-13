import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent

# Definir la clase Mascotas
class Mascotas(Persistent):
    def __init__(self, tipo, raza, edad, peso, nombre):
        self.tipo = tipo
        self.raza = raza
        self.edad = edad
        self.peso = peso
        self.nombre = nombre
        
# Establecer conexión
storage = ZODB.FileStorage.FileStorage('1dam.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# Recuperar y modificar un objeto
mascota = root.get('gato') # Recuperar la mascota almacenada con la clave 'Ave'
if mascota:
    print("Antes de la modificación:")
    print(f"Nombre: {mascota.nombre}, Raza: {mascota.raza}")
    # Modificar el atributo 'raza'
    mascota.raza = 'Siames'
    transaction.commit() # Confirmar los cambios en la base de datos
    print("Después de la modificación:")
    print(f"Nombre: {mascota.nombre}, Raza: {mascota.raza}")
else:
    print("La mascota no se encontró en la base de datos.")
    
# Cerrar la conexión
connection.close()
db.close()