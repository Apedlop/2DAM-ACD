import logging
import transaction
from ZODB import DB, FileStorage
from persistent import Persistent

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_mascotas.log"),  # Logs guardados en un archivo
        logging.StreamHandler(),  # Logs también en consola
    ]
)

class Mascota(Persistent):
    """Clase que representa una mascota."""
    def __init__(self, nombre, tipo, raza, edad, peso):
        self.nombre = nombre
        self.tipo = tipo
        self.raza = raza
        self.edad = edad
        self.peso = peso

class DatabaseManagerMascotas:
    """Componente para gestionar bases de datos orientadas a objetos con ZODB."""
    def __init__(self, filepath="mascotas.fs"):
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
            if "mascotas" not in self.root:
                self.root["mascotas"] = {}
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

    def crear_mascota(self, id, nombre, tipo, raza, edad, peso):
        """Crea y almacena una nueva mascota."""
        try:
            if id in self.root["mascotas"]:
                raise ValueError(f"Ya existe una mascota con ID {id}.")
            self.root["mascotas"][id] = Mascota(nombre, tipo, raza, edad, peso)
            logging.info(f"Mascota con ID {id} creada exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear la mascota con ID {id}: {e}")

    def leer_mascotas(self):
        """Lee y muestra todas las mascotas almacenadas."""
        try:
            mascotas = self.root["mascotas"]
            for id, mascota in mascotas.items():
                logging.info(
                    f"ID: {id}, Nombre: {mascota.nombre}, Tipo: {mascota.tipo}, "
                    f"Raza: {mascota.raza}, Edad: {mascota.edad}, Peso: {mascota.peso}"
                )
            return mascotas
        except Exception as e:
            logging.error(f"Error al leer las mascotas: {e}")

    def actualizar_mascota(self, id, nombre, tipo, raza, edad, peso):
        """Actualiza los atributos de una mascota."""
        try:
            mascota = self.root["mascotas"].get(id)
            if not mascota:
                raise ValueError(f"No existe una mascota con ID {id}.")
            mascota.nombre = nombre
            mascota.tipo = tipo
            mascota.raza = raza
            mascota.edad = edad
            mascota.peso = peso
            logging.info(f"Mascota con ID {id} actualizada exitosamente.")
        except Exception as e:
            logging.error(f"Error al actualizar la mascota con ID {id}: {e}")

    def eliminar_mascota(self, id):
        """Elimina una mascota por su ID."""
        try:
            if id not in self.root["mascotas"]:
                raise ValueError(f"No existe una mascota con ID {id}.")
            del self.root["mascotas"][id]
            logging.info(f"Mascota con ID {id} eliminada exitosamente.")
        except Exception as e:
            logging.error(f"Error al eliminar la mascota con ID {id}: {e}")

if __name__ == "__main__":
    manager = DatabaseManagerMascotas()
    manager.conectar()
    try:
        # 1) Insertar tres objetos (controlado con transacciones)
        manager.iniciar_transaccion()
        manager.crear_mascota(1, "Rex", "Perro", "Pastor Alemán", 3, 15.0)
        manager.crear_mascota(2, "Mimi", "Gato", "Siames", 2, 5.0)
        manager.crear_mascota(3, "Coco", "Perro", "Labrador", 5, 20.0)
        manager.confirmar_transaccion()

        # 2) Mostrar todos los objetos
        logging.info("Mostrando todas las mascotas después de inserciones:")
        manager.leer_mascotas()

        # 3) Intentar insertar un objeto con un ID ya creado (controlado con transacciones)
        manager.iniciar_transaccion()
        manager.crear_mascota(1, "Luna", "Gato", "Persa", 1, 4.0)  # ID 1 ya existe
        manager.confirmar_transaccion()

        # 4) Mostrar todos los objetos
        logging.info("Mostrando todas las mascotas después de intentar insertar un ID duplicado:")
        manager.leer_mascotas()

        # 5) Actualizar un objeto cambiando cualquier atributo (controlado con transacciones)
        manager.iniciar_transaccion()
        manager.actualizar_mascota(2, "Mimi", "Gato", "Siames", 3, 6.0)  # Actualizando edad y peso
        manager.confirmar_transaccion()

        # 6) Mostrar todos los objetos
        logging.info("Mostrando todas las mascotas después de actualizar un objeto:")
        manager.leer_mascotas()

        # 7) Eliminar un objeto con ID que no exista (controlado con transacciones)
        manager.iniciar_transaccion()
        manager.eliminar_mascota(10)  # ID 10 no existe
        manager.revertir_transaccion()

        # 8) Mostrar todos los objetos
        logging.info("Mostrando todas las mascotas después de intentar eliminar un ID inexistente:")
        manager.leer_mascotas()

    except Exception as e:
        logging.error(f"Error general: {e}")
        manager.revertir_transaccion()
    finally:
        manager.desconectar()