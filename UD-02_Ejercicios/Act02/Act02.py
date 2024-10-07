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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mascotas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tipo VARCHAR(50) NOT NULL,
            raza VARCHAR(50),
            edad INT,
            peso DECIMAL(5, 2),
            nombre VARCHAR(50) NOT NULL
        )               
    """)

    # Insertar datos en la tabla Mascotas
    cursor.execute(
        "INSERT INTO Mascotas (tipo, raza, edad, peso, nombre) VALUES (%s, %s, %s, %s, %s)", 
        ("Gato", "Siamés", 2, 4.5, "Luna")
    )

    # Confirmar la transacción
    conexion.commit()

    # Ejecutar consulta SELECT para ver los datos insertados
    cursor.execute("SELECT * FROM Mascotas")

    # Imprimir todas las filas obtenidas
    for fila in cursor.fetchall():
        print(fila)

except Error as e:
    print(f"Error de conexión o ejecución: {e}")

finally:
    # Verificar si la conexión está abierta y cerrarla
    if conexion.open:
        cursor.close()  # Cerrar el cursor
        conexion.close()  # Cerrar la conexión
        print("Conexión cerrada")
