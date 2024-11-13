import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent


# Definición de la clase Movil
class Movil(Persistent):
    def __init__(self, marca, modelo, anio_lanzamiento, sistema_operativo):
        self.marca = marca
        self.modelo = modelo
        self.anio_lanzamiento = anio_lanzamiento
        self.sistema_operativo = sistema_operativo
        
        
# Establecer conexión a la base de datos ZODB
storage = ZODB.FileStorage.FileStorage('moviles.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()   

# Inicializa la raíz si está vacía
if not hasattr(root, 'moviles'):
    root.moviles = {}

# Recuperar y modificar un objeto
root['moviles'].get("movil1")
if Movil:
    print("Antes de la modificación:")
    print(f"Marca: {Movil.marca}, Modelo: {Movil.modelo}, Año de lanzamiento: {Movil.anio_lanzamiento}, Sistema Operativo: {Movil.sistema_operativo}")
    # Modificar el atributo 'material'
    Movil.sistema_operativo = 'Android raro'
    transaction.commit() # Confirmar los cambios en la base de datos
    print("Después de la modificación:")
    print(f"Marca: {Movil.marca}, Modelo: {Movil.modelo}, Año de lanzamiento: {Movil.anio_lanzamiento}, Sistema Operativo: {Movil.sistema_operativo}")
else:
    print("el movil no se encontró en la base de datos.")
# Cerrar la conexión
connection.close()
db.close()