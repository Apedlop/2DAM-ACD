import pymysql
from pymysql import Error

try:
    # Conectar a la base de datos
    conexion = pymysql.connect(
        host="localhost",
        user="usuario",        # tu usuario MySQL
        password="usuario",     # tu contraseña MySQL
        database="1dam"         # la base de datos donde está la tabla Mascotas
    )

    # Crear un cursor
    cursor = conexion.cursor()

    # Iniciar la transacción
    print("Iniciando transacción...")

    # Insertar un nuevo registro en la tabla Mascotas (forzando un fallo)
    # El fallo se fuerza omitiendo uno de los valores requeridos
    sql_insert = """
    INSERT INTO Mascotas (tipo, raza, edad, peso, nombre, dueño_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    # Forzamos un error pasando solo 4 valores en lugar de 5
    datos_mascotas = ('Perro', 'Labrador', 3, 25.50, "Yoyo", 6)  # Insertamos un dueño_id que no existe
    cursor.execute(sql_insert, datos_mascotas)

    # Hacer commit si todo va bien (no debería ejecutarse en este caso)
    conexion.commit()
    print("Transacción exitosa: Registro insertado correctamente.")

except Error as e:
    # Si ocurre un error, hacer rollback
    print(f"Error en la transacción: {e}")
    if conexion:
        conexion.rollback()
        print("Se realizó rollback.")

finally:
    # Cerrar el cursor y la conexión si están abiertos
    if conexion:
        cursor.close()
        conexion.close()
        print("Conexión cerrada.")
