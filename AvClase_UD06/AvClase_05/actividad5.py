import logging
import transaction
from ZODB import DB, FileStorage
from persistent import Persistent
# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_object.log"), # Logs guardados en un archivo
        logging.StreamHandler(), # Logs también en consola
    ]
)

class Viaje(Persistent):
    def __init__(self, id, destino, duracion, tipo_viaje, precio, fecha_salida):
        self.id = id
        self.destino = destino
        self.duracion = duracion
        self.tipo_viaje = tipo_viaje
        self.precio = precio
        self.fecha_salida = fecha_salida

class DatabaseManagerObject:
    """Componente para gestionar bases de datos orientadas a objetos con ZODB."""
    def __init__(self, filepath="1dam.fs"):
        self.filepath = filepath
        self.db = None
        self.connection = None
        self.root = None
        self.transaccion_iniciada = False

    def conectar(self):
        """Conecta a la base de datos ZODB."""
        try:
            storage = FileStorage.FileStorage(self.filepath)
            self.db = DB(storage)
            self.connection = self.db.open()
            self.root = self.connection.root()
            if "viajes" not in self.root:
                self.root["viajes"] = {}
                transaction.commit()
            logging.info("Conexión establecida con ZODB.")
        except Exception as e:
            logging.error(f"Error al conectar a ZODB: {e}")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        try:
            if self.connection:
                self.connection.close()
                self.db.close()
                logging.info("Conexión a ZODB cerrada.")
        except Exception as e:
            logging.error(f"Error al cerrar la conexión a ZODB: {e}")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        try:
            transaction.begin()
            self.transaccion_iniciada = True
            logging.info("Transacción iniciada.")
        except Exception as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirma la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.commit()
                self.transaccion_iniciada = False
                logging.info("Transacción confirmada.")
            except Exception as e:
                logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revierte la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.abort()
                self.transaccion_iniciada = False
                logging.info("Transacción revertida.")
            except Exception as e:
                logging.error(f"Error al revertir la transacción: {e}")

    def crear_viaje(self, id, destino, duracion, tipo_viaje, precio, fecha_salida):
        """Crea y almacena un nuevo viaje."""
        try:
            if id in self.root["viajes"]:
                raise ValueError(f"Ya existe un viaje con ID {id}.")
            self.root["viajes"][id] = Viaje(id, destino, duracion, tipo_viaje, precio, fecha_salida)
            logging.info(f"Viaje con ID {id} creado exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear el viaje con ID {id}: {e}")

    def leer_viajes(self):
        """Lee y muestra todos los viajes almacenados."""
        try:
            viajes = self.root["viajes"]
            for id, viaje in viajes.items():
                logging.info(f"ID: {viaje.id}, Destino: {viaje.destino}, Duración: {viaje.duracion}, Tipo de Viaje: {viaje.tipo_viaje}, Precio: {viaje.precio}, Fecha de Salida: {viaje.fecha_salida}")
            return viajes
        except Exception as e:
            logging.error(f"Error al leer los viajes: {e}")

    def actualizar_viaje(self, id, destino, duracion, tipo_viaje, precio, fecha_salida):
        """Actualiza los atributos de un viaje."""
        try:
            viaje = self.root["viajes"].get(id)
            if not viaje:
                raise ValueError(f"No existe un viaje con ID {id}.")
            viaje.destino = destino
            viaje.duracion = duracion
            viaje.tipo_viaje = tipo_viaje
            viaje.precio = precio
            viaje.fecha_salida = fecha_salida
            logging.info(f"Viaje con ID {id} actualizado exitosamente.")
        except Exception as e:
            logging.error(f"Error al actualizar el viaje con ID {id}: {e}")

    def eliminar_viaje(self, id):
        """Elimina un viaje por su ID."""
        try:
            if id not in self.root["viajes"]:
                raise ValueError(f"No existe un viaje con ID {id}.")
            del self.root["viajes"][id]
            logging.info(f"Viaje con ID {id} eliminado exitosamente.")
        except Exception as e:
            logging.error(f"Error al eliminar el viaje con ID {id}: {e}")  



if __name__ == "__main__":
    manager = DatabaseManagerObject()
    manager.conectar()
    try:
        # 1) Inserta tres objetos (controlado con transacciones)
        manager.iniciar_transaccion()
        manager.crear_viaje(1, 'Helsinki', '10', 'Negocios', 200, '2023-10-19')
        manager.crear_viaje(2, 'Bilbao', '2', 'Turismo', 30, '2020-02-20')
        manager.crear_viaje(3, 'Roterdam', 16, 'Negocios', 2000, '2019-12-01')
        manager.confirmar_transaccion()
    except Exception as e:
        logging.error(f"Error general: {e}")
        manager.revertir_transaccion()

    # 2) Muestra todos los objetos
    manager.leer_viajes()

    try:
        # 3) Intenta insertar un objeto con un ID ya creado (controlado con transacciones)
        manager.iniciar_transaccion()
        manager.crear_viaje(1, 'Granada', 3, 'Turismo', 250, '2024-12-20')  
        manager.confirmar_transaccion()
    except Exception as e:
        logging.error(f"Error general: {e}")
        manager.revertir_transaccion()

    # 4) Muestra todos los objetos
    manager.leer_viajes()

    try:
        # 5) Actualiza un objeto cambiando cualquier atributo (controlado con transacciones)
        manager.iniciar_transaccion()
        manager.actualizar_viaje(2, 'Bilbao', '4', 'Negocios', 100, '2024-01-01')
        manager.confirmar_transaccion()
    except Exception as e:
        logging.error(f"Error general: {e}")
        manager.revertir_transaccion()

    # 6) Muestra todos los objetos
    manager.leer_viajes()

    try:
        # 7) Elimina un objeto con ID que no existe (controlado con transacciones)
        manager.iniciar_transaccion()
        manager.eliminar_viaje(99)  
        manager.confirmar_transaccion()
    except Exception as e:
        logging.error(f"Error general: {e}")
        manager.revertir_transaccion()

    # 8) Muestra todos los objetos
    manager.leer_viajes()

    manager.desconectar()