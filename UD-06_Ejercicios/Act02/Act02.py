import logging
import mysql.connector
from mysql.connector import Error

# Configuración de logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    handlers = [
        logging.FileHandler("databasemanager.log"),  # Logs guardados en un archivo
        logging.StreamHandler(),  # Logs también en consola
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
                self.connection.autocommit = False  # Desactiva el autocommit
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

    def crear_mascota(self, tipo, raza, edad, peso, nombre):
        """Insertar una nueva mascota en la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO Mascotas (tipo, raza, edad, peso, nombre)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (tipo, raza, edad, peso, nombre))
            logging.info(f"Mascota '{nombre}' insertada exitosamente.")
        except Error as e:
            logging.error(f"Error al insertar la mascota '{nombre}': {e}")

    def leer_mascotas(self):
        """Leer todas las mascotas de la base de datos"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Mascotas")
            mascotas = cursor.fetchall()
            logging.info("Mascotas recuperadas:")
            for mascota in mascotas:
                logging.info(mascota)
            return mascotas
        except Error as e:
            logging.error(f"Error al leer las mascotas: {e}")
            return None

    def actualizar_mascota(self, id, tipo, raza, edad, peso, nombre):
        """Actualizar una mascota en la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE Mascotas
                SET tipo = %s, raza = %s, edad = %s, peso = %s, nombre = %s
                WHERE id = %s
            """
            cursor.execute(query, (tipo, raza, edad, peso, nombre, id))
            logging.info(f"Mascota con ID {id} actualizada exitosamente.")
        except Error as e:
            logging.error(f"Error al actualizar la mascota con ID {id}: {e}")

    def eliminar_mascota(self, id):
        """Eliminar una mascota de la base de datos"""
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Mascotas WHERE id = %s"
            cursor.execute(query, (id,))
            logging.info(f"Mascota con ID {id} eliminada exitosamente.")
        except Error as e:
            logging.error(f"Error al eliminar la mascota con ID {id}: {e}")

    def iniciar_transaccion(self):
        """Iniciar una transacción"""
        try:
            if not self.transaccion_activa:
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

# Ejemplo de uso del componente DatabaseManager para la clase Mascota
if __name__ == "__main__":
    db_manager = DatabaseManager("localhost", "usuario", "usuario", "1dam")
    db_manager.conectar()
    try:
        # Crear una mascota
        db_manager.iniciar_transaccion()
        db_manager.crear_mascota("Perro", "Labrador", 3, 25.5, "Rex")
        db_manager.confirmar_transaccion()

        # Leer mascotas
        mascotas = db_manager.leer_mascotas()

        # Actualizar una mascota
        db_manager.iniciar_transaccion()
        db_manager.actualizar_mascota(1, "Perro", "Labrador", 4, 26.0, "Rex")
        db_manager.confirmar_transaccion()

        # Eliminar una mascota
        db_manager.iniciar_transaccion()
        db_manager.eliminar_mascota(1)
        db_manager.confirmar_transaccion()

        # Bloque con transacción revertida
        db_manager.iniciar_transaccion()
        db_manager.crear_mascota("Gato", "Persa", 2, 4.5, "Luna")
        db_manager.revertir_transaccion()

    except Exception as e:
        logging.error(f"Se produjo un error: {e}")
        if db_manager.transaccion_activa:
            db_manager.revertir_transaccion()
    finally:
        db_manager.desconectar()
