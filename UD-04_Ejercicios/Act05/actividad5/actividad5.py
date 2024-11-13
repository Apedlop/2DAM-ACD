from ZODB import DB, FileStorage
from persistent import Persistent
import transaction

# Clases para Mascotas y Dueños
class Mascotas(Persistent):
    def __init__(self, tipo, raza, edad, peso, nombre, id_dueño):
        self.tipo = tipo
        self.raza = raza
        self.edad = edad
        self.peso = peso
        self.nombre = nombre
        self.id_dueño = id_dueño  # ID del dueño

class Dueños(Persistent):
    def __init__(self, nombre_dueño, direccion, telefono):
        self.nombre_dueño = nombre_dueño
        self.direccion = direccion
        self.telefono = telefono

# Conectar a la base de datos ZODB
storage = FileStorage.FileStorage('1dam.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

# Verificar y crear colecciones si no existen
if 'mascotas' not in root:
    root['mascotas'] = {}

if 'dueños' not in root:
    root['dueños'] = {}

# Insertar datos en Dueños
root['dueños']['Dueño1'] = Dueños("Dueño1", "Calle Falsa 123", "123-456-789")
root['dueños']['Dueño2'] = Dueños("Dueño2", "Avenida Real 456", "987-654-321")

# Insertar datos en Mascotas, incluyendo el id_dueño
root['mascotas']['Perro'] = Mascotas("Perro", "Border Collie", 9, 12.6, "Cloe", "Dueño1")
root['mascotas']['Gato'] = Mascotas("Gato", "Persa", 4, 5.2, "Bigotes", "Dueño1")
root['mascotas']['Pez'] = Mascotas("Pez", "Dorado", 1, 0.2, "Doradito", "Dueño2")

# Confirmar la transacción
transaction.commit()

# Mostrar las mascotas pertenecientes a "Dueño1"
print("Mascotas de Dueño1:")
for mascota in root['mascotas'].values():
    if mascota.id_dueño == "Dueño1":
        print(f"{mascota.tipo} - {mascota.nombre}, Raza: {mascota.raza}, Edad: {mascota.edad}, Peso: {mascota.peso} kg")

# Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()
