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
    
    # Actualizar datos
    cursor.execute("UPDATE Mascotas SET edad = %s WHERE nombre = %s", (8, 'Luna'))

    # Confirmar la transacción
    conexion.commit()
    
    print(cursor.rowcount, "registro(s) actualizado(s)")

except Error as e:
    print(f"Error de conexión o ejecución: {e}")

finally:
    # Verificar si la conexión está abierta y cerrarla
    if conexion.open:
        cursor.close()  # Cerrar el cursor
        conexion.close()  # Cerrar la conexión
        print("Conexión cerrada")