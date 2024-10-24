from peewee import MySQLDatabase, Model, CharField, IntegerField, DecimalField

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

# Definir la tabla 'Mascota' con los campos especificados
class Mascota(Model):
    tipo = CharField(max_length=50)  # Tipo de mascota (Perro, Gato, etc.)
    raza = CharField(max_length=50)  # Raza de la mascota
    edad = IntegerField(null=True)  # Edad de la mascota
    peso = DecimalField(max_digits=5, decimal_places=2)  # Peso de la mascota
    nombre = CharField(max_length=50)  # Nombre de la mascota

    class Meta:
        database = db
        table_name = 'Mascotas'

# TAREA 1: Recuperar y mostrar mascotas de tipo específico
print("Tarea1...")

# Recuperar mascotas de tipo 'Perro'
mascotas_perros = Mascota.select().where(Mascota.tipo == 'Perro')

# Mostrar dos atributos de cada mascota (nombre y raza)
for mascota in mascotas_perros:
    print(f"Nombre: {mascota.nombre}, Raza: {mascota.raza}")

# TAREA 2: Eliminar un solo registro en base a dos atributos
print("Tarea2...")

# Eliminar la mascota con raza 'Labrador' y nombre 'Max'
Mascota.delete().where((Mascota.raza == 'Labrador') & (Mascota.nombre == 'Max')).execute()
print("Eliminación realizada con éxito")

# TAREA 3: Eliminar todos los registros que cumplan una condición
print("Tarea3...")

# Eliminar todas las mascotas de tipo 'Gato'
Mascota.delete().where(Mascota.tipo == 'Gato').execute()

# Mostrar los registros restantes para verificar la eliminación
mascotas_restantes = Mascota.select()
for mascota in mascotas_restantes:
    print(f"Nombre: {mascota.nombre}, Tipo: {mascota.tipo}")

# Cerrar la conexión a la base de datos
db.close()
print("Conexión cerrada.")
