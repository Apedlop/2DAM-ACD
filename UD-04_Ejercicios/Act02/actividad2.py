import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent

# Definir clase Mascotas
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

# Almacenar una mascota
root['perro'] = Mascotas('Perro', 'Bodeguero', 3, 9.5, 'Yoyo')
root['gato'] = Mascotas('Gato', 'Persa', 2, 4.0, 'Blanquita')
root['conejito'] = Mascotas('Conejo', 'Enano', 1, 1.5, 'Nube')

# Guardar cambios en la base de datos
transaction.commit()

# Filtrar mascotas por tipo
tipo_deseado = "Perro"
for clave, mascota in root.items():
    if hasattr(mascota, 'tipo') and mascota.tipo == tipo_deseado:
        print(f"Tipo: {mascota.tipo}, Raza: {mascota.raza}, Edad: {mascota.edad}, Peso: {mascota.peso}, Nombre: {mascota.nombre}")

# Cerrar conexión
connection.close()
db.close()