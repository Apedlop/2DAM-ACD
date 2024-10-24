from peewee import MySQLDatabase, Model, CharField, IntegerField, DecimalField, IntegrityError


# Configurar la base de datos
db = MySQLDatabase(
    '1dam',  # Nombre de la base de datos
    user='usuario',  # Usuario de MySQL
    password='usuario',  # Contraseña de MySQL
    host='localhost',  # Host
    port=3306  # Puerto de MySQL
)

# Conectar a la base de datos
db.connect()
print("Conexión exitosa a la base de datos.")


# Definir la tabla 'Mascotas' con los campos especificados
class Mascotas(Model):
    tipo = CharField(max_length=50)  # Tipo de mascota
    raza = CharField(max_length=50)  # Raza de la mascota
    edad = IntegerField(null=True)  # Edad de la mascota
    peso = DecimalField(max_digits=5, decimal_places=2)  # Peso de la mascota
    nombre = CharField(max_length=50)  # Nombre de la mascota

    class Meta:
        database = db
        table_name = 'Mascotas'


# Función para verificar si la tabla existe
def tabla_existe(nombre_tabla):
    consulta = """SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"""
    cursor = db.execute_sql(consulta, ('1dam', nombre_tabla))
    resultado = cursor.fetchone()
    return resultado[0] > 0


# Eliminar la tabla si ya existe
if tabla_existe(Mascotas._meta.table_name):
    print(f"La tabla '{Mascotas._meta.table_name}' existe.")
    db.drop_tables([Mascotas], cascade=True)
    print(f"Tabla '{Mascotas._meta.table_name}' eliminada con éxito.")
else:
    print(f"La tabla '{Mascotas._meta.table_name}' no existe.")

# Crear la tabla 'Mascotas'
db.create_tables([Mascotas])
print("Tabla 'Mascotas' creada o ya existente.")

# Iniciar una transacción para insertar registros
try:
    # Usar db.atomic() para asegurar la transacción, si ocurre algún error se deshacen los cambios
    with db.atomic():
        # Insertar varios registros en la tabla 'Mascotas'
        Mascotas.create(nombre='Firulais', tipo='Perro', raza='Pastor Alemán', edad=5, peso=35.50)
        Mascotas.create(nombre='Miau', tipo='Gato', raza='Siames', edad=3, peso=4.30)
        Mascotas.create(nombre='Dory', tipo='Pez', raza='Cirujano', edad=1, peso=0.50)
        Mascotas.create(nombre='Bugs', tipo='Conejo', raza='Angora', edad=2, peso=1.75)
        Mascotas.create(nombre='Charlie', tipo='Ave', raza='Loro', edad=4, peso=0.60)

        print("Registros insertados en la tabla 'Mascotas' con éxito.")
except IntegrityError as e:
    # Manejar el error en caso de que ocurra
    print(f"Error al insertar registros en la tabla 'Mascotas': {e}")

# Cerrar la conexión a la base de datos
db.close()
print("Conexión cerrada.")