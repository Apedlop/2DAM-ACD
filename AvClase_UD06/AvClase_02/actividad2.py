import logging
import mysql.connector
from mysql.connector import Error
# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager.log"), # Logs guardados en un archivo
        logging.StreamHandler(), # Logs también en consola
    ]
)

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.transaccion_activa = False
        
    def conectar(self):
        """Conectar a la base de datos MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.connection.autocommit = False # Desactiva el autocommit
                logging.info("Conexión exitosa a la base de datos.")
        except Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            
    def desconectar(self):
        """Cerrar la conexión a la base de datos"""
        if self.connection and self.connection.is_connected():
            if self.transaccion_activa:
                logging.warning("Cerrando conexión con una transacción activa. Revirtiendo...")
                self.revertir_transaccion()
            self.connection.close()
            logging.info("Conexión cerrada.")
        
    def crear_viaje(self, destino, duracion, tipo_viaje, precio, fecha_salida):
        """Insertar un nuevo viaje en la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO Viajes (destino, duracion, tipo_viaje, precio, fecha_salida)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (destino, duracion, tipo_viaje, precio, fecha_salida))
            logging.info(f"Viaje '{destino}' insertada exitosamente.")
        except Error as e:
            logging.error(f"Error al insertar el viaje '{destino}': {e}")
                
    def leer_viajes(self):
        """Leer todos los viajes de la base de datos"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Viajes")
            viajes = cursor.fetchall()
            logging.info("Viajes recuperados:")
            for viaje in viajes:
                logging.info(viaje)
            return viajes
        except Error as e:
            logging.error(f"Error al leer los viajes: {e}")
            return None
            
            
    def actualizar_viaje(self, id, destino, duracion, tipo_viaje, precio, fecha_salida):
        """Actualizar un viaje en la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE Viajes
                SET destino = %s, duracion = %s, tipo_viaje = %s, precio = %s, fecha_salida = %s
                WHERE id = %s
            """
            cursor.execute(query, (destino, duracion, tipo_viaje, precio, fecha_salida, id))
            logging.info(f"Viaje con ID {id} actualizado exitosamente.")
        except Error as e:
            logging.error(f"Error al actualizar el viaje con ID {id}: {e}")
                
    def eliminar_viaje(self, id):
        """Eliminar un viaje de la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Viajes WHERE id = %s"
            cursor.execute(query, (id,))
            logging.info(f"Viajes con ID {id} eliminado exitosamente.")
        except Error as e:
            logging.error(f"Error al eliminar el viaje con ID {id}: {e}")
            
    def iniciar_transaccion(self):
        """Iniciar una transacción"""
        try:
            if not self.transaccion_activa:
                #self.connection.rollback()
                #self.connection.start_transaction()
                self.transaccion_activa = True
                logging.info("Transacción iniciada.")
            else:
                logging.warning("Transacción ya en curso. No se puede iniciar otra.")
        except Error as e:
            logging.error(f"Error al iniciar la transacción: {e}")
            raise
        
    def confirmar_transaccion(self):
        """Confirmar (commit) una transacción"""
        try:
            if self.transaccion_activa:
                self.connection.commit()
                self.transaccion_activa = False
                logging.info("Transacción confirmada.")
            else:
                logging.warning("No hay ninguna transacción activa para confirmar.")
        except Error as e:
            logging.error(f"Error al confirmar la transacción: {e}")
            raise
        
    def revertir_transaccion(self):
        """Revertir (rollback) una transacción"""
        try:  
            if self.transaccion_activa:
                self.connection.rollback()
                self.transaccion_activa = False
                logging.info("Transacción revertida.")
            else:
                logging.warning("No hay ninguna transacción activa para revertir.")
        except Error as e:
            logging.error(f"Error al revertir la transacción: {e}")
            raise
        
if __name__ == "__main__":
    db_manager = DatabaseManager("localhost", "usuario", "usuario", "1dam")
    db_manager.conectar()
    try:
        # Bloque de inserción
        db_manager.iniciar_transaccion()
        db_manager.crear_viaje("Madrid", 12, "Negocios", 205, '2022-03-14')
        db_manager.confirmar_transaccion()
        
        # Leer datos (no requiere transacción)
        herramientas = db_manager.leer_viajes()
        
        # Bloque de actualización
        db_manager.iniciar_transaccion()
        db_manager.actualizar_viaje(1, "Madrid", 12, "Negocios", 250, '2022-03-14')
        db_manager.confirmar_transaccion()
        
        # Bloque de eliminación
        db_manager.iniciar_transaccion()
        db_manager.eliminar_viaje(1)
        db_manager.confirmar_transaccion()
        
        # Bloque con transacción revertida
        db_manager.iniciar_transaccion()
        db_manager.crear_viaje("Barcelona", 5, "Turismo", 100, "2025-03-10")
        db_manager.revertir_transaccion()
    except Exception as e:
        logging.error(f"Se produjo un error: {e}")
        if db_manager.transaccion_activa:
            db_manager.revertir_transaccion()
    finally:
        db_manager.desconectar()
        