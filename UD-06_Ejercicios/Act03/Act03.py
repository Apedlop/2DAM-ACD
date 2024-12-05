import logging
from peewee import Model, CharField, ForeignKeyField, MySQLDatabase

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_orm.log"),
        logging.StreamHandler()
    ]
)

# Configuración de la base de datos MySQL
db = MySQLDatabase(
    "1dam",  # Nombre de la base de datos
    user="usuario",  # Usuario de MySQL
    password="usuario",  # Contraseña de MySQL
    host="localhost",  # Host
    port=3306  # Puerto por defecto de MySQL
)

# Modelos de la base de datos
class Proveedor(Model):
    nombre = CharField()
    direccion = CharField()

    class Meta:
        database = db

class Herramienta(Model):
    nombre = CharField()
    tipo = CharField()
    marca = CharField()
    uso = CharField()
    material = CharField()
    proveedor = ForeignKeyField(Proveedor, backref='herramientas')

    class Meta:
        database = db

# Componente DatabaseManagerORM
class DatabaseManagerORM:
    def __init__(self):
        self.db = db

    def conectar(self):
        """Conecta la base de datos y crea las tablas."""
        self.db.connect()
        self.db.create_tables([Proveedor, Herramienta])
        logging.info("Conexión establecida y tablas creadas.")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if not self.db.is_closed():
            self.db.close()
            logging.info("Conexión cerrada.")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        self.db.begin()
        logging.info("Transacción iniciada.")

    def confirmar_transaccion(self):
        """Confirma (commit) una transacción."""
        self.db.commit()
        logging.info("Transacción confirmada.")

    def revertir_transaccion(self):
        """Revierte (rollback) una transacción."""
        self.db.rollback()
        logging.info("Transacción revertida.")

    def crear_proveedor(self, nombre, direccion):
        """Inserta un nuevo proveedor."""
        proveedor = Proveedor.create(nombre=nombre, direccion=direccion)
        logging.info(f"Proveedor creado: {proveedor.nombre} - {proveedor.direccion}")
        return proveedor

    def crear_herramienta(self, nombre, tipo, marca, uso, material, proveedor):
        """Inserta una nueva herramienta."""
        herramienta = Herramienta.create(
            nombre=nombre, tipo=tipo, marca=marca, uso=uso, material=material, proveedor=proveedor
        )
        logging.info(f"Herramienta creada: {herramienta.nombre} - {herramienta.tipo}")
        return herramienta

    def leer_herramientas(self, proveedor):
        """Lee todas las herramientas asociadas a un proveedor."""
        herramientas = Herramienta.select().where(Herramienta.proveedor == proveedor)
        logging.info("Leyendo herramientas:")
        for herramienta in herramientas:
            logging.info(f"{herramienta.nombre} - {herramienta.tipo} ({herramienta.proveedor.nombre})")
        return herramientas

    def actualizar_proveedor(self, proveedor, nuevo_contacto):
        """Actualiza el contacto de un proveedor."""
        proveedor.direccion = nuevo_contacto
        proveedor.save()
        logging.info(f"Proveedor actualizado: {proveedor.nombre} - {proveedor.direccion}")
        return proveedor

    def eliminar_proveedor(self, proveedor):
        """Elimina un proveedor."""
        proveedor.delete_instance()
        
    def actualizar_herramienta(self, herramienta, nuevo_tipo):
        """Actualiza el tipo de una herramienta."""
        herramienta.tipo = nuevo_tipo
        herramienta.save()
        return herramienta

    def eliminar_herramienta(self, herramienta):
        """Elimina una herramienta."""
        herramienta.delete_instance()
        logging.info(f"Herramienta eliminada: {herramienta.nombre}")

if __name__ == "__main__":
    db_manager = DatabaseManagerORM()
    db_manager.conectar()
    try:
        # Creación de dos proveedores
        print("Gestión de Proveedores:")
        db_manager.iniciar_transaccion()
        proveedor_a = db_manager.crear_proveedor("Proveedor A", "123-456-789")
        proveedor_b = db_manager.crear_proveedor("Proveedor B", "987-654-321")
        db_manager.confirmar_transaccion()
        
        # Cambiar dato por mi DNI
        print("Cambio del dato por mi DNI 20094042 al proveedor A")
        db_manager.iniciar_transaccion()
        db_manager.actualizar_proveedor(proveedor_a, "20094042")
        db_manager.confirmar_transaccion()
        
        # Eliminar al Proveedor B
        print("Eliminar al Proveedor B")
        db_manager.iniciar_transaccion()
        db_manager.eliminar_proveedor(proveedor_b)
        db_manager.confirmar_transaccion()
        
        # Gestión de Herramientas
        print("Gestión de Herramientas:")
        db_manager.iniciar_transaccion()
        herramienta_1 = db_manager.crear_herramienta("Martillo", "Manual", "Marca1", "Construcción", "Acero", proveedor_a)
        herramienta_2 = db_manager.crear_herramienta("Taladro", "Eléctrico", "Marca3", "Reformas", "Acero", proveedor_a)
        db_manager.confirmar_transaccion()
        
        # Consultar herramientas asociadas al proveedor A
        print("Herramientas asociadas al proveedor Proveedor A:")
        herramientas_a = db_manager.leer_herramientas(proveedor_a)
        
        # Actualizar herramienta Martillo a tipo Reforzado
        print("Actualizar herramienta Martillo a tipo Reforzado")
        db_manager.iniciar_transaccion()
        db_manager.actualizar_herramienta(herramienta_1, "Reforzado")
        db_manager.confirmar_transaccion()
        
        # Eliminar herramienta Taladro
        print("Eliminar herramienta Taladro")
        db_manager.iniciar_transaccion()
        db_manager.eliminar_herramienta(herramienta_2)
        db_manager.confirmar_transaccion()

    finally:
        db_manager.desconectar()
