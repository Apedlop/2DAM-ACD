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

    # Generar 10000 datos aleatorios
    for i in range(10000):
        tipo = f"Tipo{i+1}"
        raza = random.choice(['Labrador', 'Bulldog', 'Beagle', 'Pastor Alemán', 'Golden Retriever', 'Poodle'])
        nombre = random.choice(['Max', 'Bella', 'Charlie', 'Luna', 'Rocky', 'Simba', 'Chloe', 'Coco', 'Milo', 'Oliver'])
        peso = round(random.uniform(5, 40), 2)  # El random.uniform genera un número decimal aleatorio
        edad = random.randint(1, 15)

        # Insertar datos en la tabla Mascotas
        cursor.execute(
            "INSERT INTO Mascotas (tipo, raza, edad, peso, nombre) VALUES (%s, %s, %s, %s, %s)", 
            (tipo, raza, edad, peso, nombre)
        )

    # Confirmar la transacción para guardar los cambios
    # conexion.commit()

    # Medir el tiempo después de las inserciones
    end_time = time.time()
    print(f"Tiempo de inserción con pymysql: {end_time - start_time} segundos")

except mysql.connector.MySQLError as e:
    print(f"Error de conexión o ejecución: {e}")

finally:
    # Verificar si la conexión está abierta y cerrarla
    if conexion.is_connected:
        cursor.close()  # Cerrar el cursor
        conexion.close()  # Cerrar la conexión
        print("Conexión cerrada")
