from ZODB import DB, FileStorage
from persistent import Persistent
import ZODB
import transaction

# Clase Mascotas para el ejemplo
class Mascotas(Persistent):
    def __init__(self, tipo, raza, edad, peso, nombre):
        self.tipo = tipo
        self.raza = raza
        self.edad = edad
        self.peso = peso
        self.nombre = nombre
        
# Conectar a la base de datos ZODB
storage = FileStorage.FileStorage('1dam.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

# Función para gestionar la inserción de varias mascotas con transacción
def agregar_mascotas():
    try:
        print("Iniciando la transacción para agregar mascotas...")
        # Verificar y crear 'mascotas' en root si no existe
        if 'mascotas' not in root:
            root['mascotas'] = {} # Inicializar una colección de mascotas si no existe
            transaction.commit() # Confirmar la creación en la base de datos
        # Crear y añadir nuevas mascotas
        mascota1 = Mascotas("Perro", "Border Collie", 9, 12.6, "Cloe")
        mascota2 = Mascotas("Gato", "Persa", 4, 5.2, "Bigotes")
        mascota3 = Mascotas("Pez", "Dorado", 1, 0.2, "Doradito")
        # Añadir mascotas a la colección en la raíz de ZODB
        root['mascotas']["Perro"] = mascota1
        root['mascotas']["Gato"] = mascota2
        root['mascotas']["Pez"] = mascota3
        # Confirmar la transacción
        transaction.commit()
        print("Transacción completada: Mascotas añadidas correctamente.")
    except Exception as e:
        # Si ocurre un error, revertimos la transacción
        transaction.abort()
        print(f"Error durante la transacción: {e}. Transacción revertida.")

# Llamar a la función para añadir mascotas
agregar_mascotas()

# Cerrar la conexión a la base de datos ZODB
connection.close()
db.close()