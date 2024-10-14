import mysql.connector
from mysql.connector import Error
import time
import random

try:
    # Establecer la conexión con la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='1dam'
    )
    
    if conexion.is_connected:
        print("Conexión a la base de datos exitosa")

    # Crear cursor para ejecutar consultas
    cursor = conexion.cursor()

    # Comenzamos a medir el tiempo
    start_time = time.time()

     # Ejecutar consulta SELECT para ver los datos insertados
    for i in range(10000):
        cursor.execute("SELECT * FROM Mascotas")
        resultado = cursor.fetchall()

    cursor.close()
    # Confirmar la transacción para guardar los cambios
    # conexion.commit()

    # Medir el tiempo después de las inserciones
    end_time = time.time()
    print(f"Tiempo de inserción con mysql.connector: {end_time - start_time} segundos")

except mysql.connector.MySQLError as e:
    print(f"Error de conexión o ejecución: {e}")

finally:
    # Verificar si la conexión está abierta y cerrarla
    if conexion.is_connected:
        cursor.close()  # Cerrar el cursor
        conexion.close()  # Cerrar la conexión
        print("Conexión cerrada")
