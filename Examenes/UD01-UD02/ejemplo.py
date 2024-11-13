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

except Error as e:
    print(f"Error de conexión: {e}")

finally:
    if conexion.open:
        conexion.close()
        print("Conexión cerrada")