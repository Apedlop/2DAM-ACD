import pymysql.cursors

conexion = pymysql.connect(host='localhost',
                           user='usuario',
                           password='usuario',
                           database='1dam',)

with conexion:
    
    with conexion.cursor() as cursor: #Para la primera consulta
        
        # Ejecutar una consulta para obtener las 5 instancias de la tabla AplicacionesMoviles
        cursor.execute("SELECT * FROM Mascotas LIMIT 5")
        
        print("Usando fetchone():")
        for i in range (5):
            fila = cursor.fetchone()
            print(fila)
            
    with conexion.cursor() as cursor2: #Para la segunda consulta
        
        cursor2.execute("SELECT * FROM Mascotas LIMIT 5")
        
        print("Usando fetchone() de nuevo:")
        for i in range (5):
            fila = cursor2.fetchone()
            print(fila)