import pymysql
from pymysql import Error

try:
    conexion = pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='1dam'
    )
    if conexion.open:
        print("Conexión a la base de datos exitosa")

    # Crear cursor para ejecutar consultas
    cursor = conexion.cursor()

    # Crear tabla Clientes
    sql_crear_Dueño = """
        CREATE TABLE IF NOT EXISTS Dueño (
        id INT AUTO_INCREMENT PRIMARY KEY,   -- Clave primaria
        nombre VARCHAR(100) NOT NULL,
        direccion VARCHAR(255),
        telefono VARCHAR(15)
        )              
    """

    cursor.execute(sql_crear_Dueño)

    # Añadir columna dueño_id a la tabla Mascotas
    sql_alter_Mascotas = """
        ALTER TABLE Mascotas ADD dueño_id INT, 
        ADD CONSTRAINT fk_dueño
        FOREIGN KEY (dueño_id) REFERENCES Mascotas(id)
    """

    cursor.execute(sql_alter_Mascotas)

    print("Relación entre Mascotas y Dueño creada.")

except Error as e:
    print(f"Error de conexión o ejecución: {e}")

finally:
    # Verificar si la conexión está abierta y cerrarla
    if conexion.open:
        cursor.close()  # Cerrar el cursor
        conexion.close()  # Cerrar la conexión
        print("Conexión cerrada")