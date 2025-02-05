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
    "1dam", # Nombre de la base de datos
    user="usuario", # Usuario de MySQL
    password="usuario", # Contraseña de MySQL
    host="localhost", # Host
    port=3306 # Puerto por defecto de MySQL
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
    
    def leer_herramientas(self):
        """Lee todas las herramientas."""
        herramientas = Herramienta.select()
        logging.info("Leyendo herramientas:")
        for herramienta in herramientas:
            logging.info(f"{herramienta.nombre} - {herramienta.tipo}({herramienta.proveedor.nombre})")
        return herramientas
    
if __name__ == "__main__":
    db_manager = DatabaseManagerORM()
    db_manager.conectar()
    print("")

    try:
        db_manager.iniciar_transaccion()
        proveedor_a = db_manager.crear_proveedor("ProveedorA", "Contacto 123-456-789")
        proveedor_b = db_manager.crear_proveedor("ProveedorB", "Contacto 987-654-321")
        db_manager.confirmar_transaccion()
        
        print("")

        db_manager.iniciar_transaccion()
        print(f"Cambio del dato por mi DNI 30277138F al proveedor A")
        proveedor_a.direccion="30277138F"
        proveedor_a.save()
        db_manager.confirmar_transaccion()
        
        print("")
        
        db_manager.iniciar_transaccion()
        print(f"Eliminar al proveedor B")
        proveedor_b.delete_instance()
        db_manager.confirmar_transaccion()
        
        print("")
        
        db_manager.iniciar_transaccion()
        martillo = db_manager.crear_herramienta("Martillo", "Manual","","","",proveedor_a)
        taladro = db_manager.crear_herramienta("Taladro", "Eléctrico","","","",proveedor_a)
        db_manager.confirmar_transaccion()
        
        print("")
        
        
        total_herramientas = db_manager.leer_herramientas()
        for herramienta in total_herramientas:
            if herramienta.proveedor == "Proveedor A":
                print(f"Nombre: {herramienta.nombre}, Tipo: {herramienta.tipo}, Marca: {herramienta.marca}, Uso: {herramienta.uso}, Material: {herramienta.material}, Proveedor: {herramienta.proveedor}")
        
        print("")
        
        db_manager.iniciar_transaccion()
        martillo.tipo = "Reforzado"
        db_manager.confirmar_transaccion()
        
        print("")
        
        
        db_manager.iniciar_transaccion()
        taladro.delete_instance()
        db_manager.confirmar_transaccion()
        
        
        
        
        
    
    except Exception as e:
        logging.error(f"Error general: {e}")
        db_manager.revertir_transaccion()


        