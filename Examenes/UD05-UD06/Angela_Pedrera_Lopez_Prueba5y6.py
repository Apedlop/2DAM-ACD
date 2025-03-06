from pymongo import MongoClient, errors
import logging
import transaction
import logging
from peewee import Model, CharField, ForeignKeyField, MySQLDatabase
from ZODB import DB, FileStorage
from persistent import Persistent

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_orm.log"),
        logging.StreamHandler()
    ]
)

# Configuración de la base de datos MongoDB
db = MongoClient(f"mongodb://{"usuario"}:{"usuario"}@{"localhost"}:{27017}/{"1dam"}", serverSelectionTimeoutMS=5000)   

class Producto(Model):
    def __init__(self, nombre, categoria, perecio, stock):
        self.nombre = nombre
        self.categoria = categoria
        self.precio = perecio
        self.stock = stock
        
    class Meta:
        database = db

class DatabaseProductManager:
    def __init__(self, db_name="1dam", collection_name="productos"):
        self.db_name = db_name
        self.collection_name = collection_name
        
        # Conectamos con MongoDB
        self.database = db[self.db_name]
        colecciones = self.database.list_collection_names()
        print(colecciones)
        logging.info("Conexión establecida con MongoDB.")
    
    def insertar_productos(self, productos):
          # Seleccionar o crear la colección 'mascotas'
        coleccion_productos = self.database["productos"]
        coleccion_productos.insert_many(productos)
      
        
    def consultar_proyeccion_ordenada(self, filtro, proyeccion, orden):
        for doc in self.database.find({}, proyeccion).sort([orden]):
            print(doc)
        
    def mostrar_todos_productos(self):
        for doc in list(self.database["productos"].find({})):
            print(doc)
        
    # def actualizar_productos(self, filtro, actualizacion):

    def contar_documentos(self):
        coleccion_productos = self.database["productos"]
        totalProductos = coleccion_productos.countDocuments()
        print(totalProductos)
        
    def eliminar_documentos(self, filtro):
        for doc in list(self.database["productos"].find({})):
            if doc.stock > filtro:
                print(doc)
        

    # def consulta_compleja(self, filtro, proyeccion, orden):

    def cerrar_conexion(self):
        try:
            self.producto.close()
            logging.info("Conexión cerrada.")
        except Exception as e:
            logging.error("Error al cerrar la conexión.")
        
db = DatabaseProductManager()
# db.desconectar()

productos = [{"nombre": "Drone Phantom X", "categoria": "Drones", "precio": 1200.50, "stock": 8},
             {"nombre": "Auriculares Sonic Boom", "categoria": "Auriculares", "precio": 299.99, "stock": 15},
             {"nombre": "Cámara Action Pro", "categoria": "Cámaras", "precio": 499.99, "stock": 10},
             {"nombre": "Asistente SmartBuddy", "categoria": "Asistentes Inteligentes", "precio": 199.99, "stock": 20},
             {"nombre": "Cargador Solar Ultra", "categoria": "Accesorios", "precio": 49.99, "stock": 3}]

# db.insertar_productos(productos)

# db.consultar_proyeccion_ordenada("Accesorios")
db.mostrar_todos_productos()
# db.contar_documentos()
db.eliminar_documentos(5)