import pymysql
from pymysql import Error
import csv, json

# Clase para JSON
class JSONFileHandler:
    # Método para leer .json
    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo JSON: {e}")

    # Método para escribir en el .json
    def write_json(self, file_path, titulo, autor, genero, año_publicacion, libreria_origen):
        try:
            with open(file_path, 'w') as f:
                data = {} # Creamos un diccionario vacío
                data["titulo"] = titulo # Añadimos al Strign DNI el valor dni
                data["autor"] = autor # Añadimos al String Fecha_Nac el valor fecha
                data["genero"] = genero
                data["año_publicacion"] = año_publicacion
                data["libreria_origen"] = libreria_origen
                json.dump(data, f) # Para crear y/o guardar en el fichero
                return data
        except Exception as e:
            print(f"Error leyendo JSON: {e}")

# Clase para CSV
class CSVFileHandler:
    # Método para leer .csv
    def read_csv(self, file_path):
        try:
            with open(file_path, mode='r', newline='') as f:
                reader = csv.DictReader(f)  # Creamos el objeto reader para leer las filas como diccionarios
                rows = []  # Lista vacía para almacenar las filas
                for row in reader:  # Recorremos cada fila en el archivo CSV
                    rows.append(row)  # Añadimos cada fila (un diccionario) a la lista
                return rows  # Devolvemos la lista con todas las filas
        except Exception as e:
            print(f"Error leyendo el archivo CSV: {e}")

    # Método para escribir en el .csv
    def write_csv(self, file_path, data, fieldnames):
        try:
            with open(file_path, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)  # Creamos un objeto writer para escribir en CSV
                writer.writeheader()  # Escribimos la primera fila que contiene los nombres de las columnas (encabezado)
                writer.writerow(data)  # Escribimos los datos en una fila en el archivo CSV
        except Exception as e:
            print(f"Error escribiendo en el archivo CSV: {e}")

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

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Libreria (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(50),
                autor VARCHAR(50),
                genero VARCHAR(50),
                año_publicacion INT,
                libreria_origen VARCHAR(50)
            )               
        """)
        print("Tabla creada")
    except Error:
        print("Error al crear la base de datos")

    # Insertar datos en la tabla 
    try:
        cursor.execute(
            "INSERT INTO Libreria (titulo, autor, genero, año_publicacion, libreria_origen) VALUES ('Don Quijote de la Mancha', 'Miguel de Cervantes', 'Novela', 5, 'Ramón Valle Inclán'), ('Cien Años de Soledad', 'Gabriel García Márquez', 'Novela', 4, 'Ramón Valle Inclán'),('Crimen y Castigo', 'Fiódor Dostoyevski', 'Novela', 6, 'Ramón Valle Inclán'),('La Casa de los Espíritus', 'Isabel Allende', 'Novela', 8, 'Ramón Valle Inclán'),('El Nombre de la Rosa', 'Umberto Eco', 'Misterio', 8, 'Ramón Valle Inclán')"
        )
        print("Inserción con exito")
    except Error:
        print("Error al insertar libros")

    # Confirmar la transacción
    conexion.commit()

    # Leer archov .csv
    origen = {"libreria_origen": "Ramón del Valle Inclán"}
    fieldnames = ["titulo", "autor", "genero", "año_publicacion", "libreria_origen"]
    csv_handler = CSVFileHandler()
    file_path = 'libros_unamuno.csv'
    # Leer los datos del archivo CSV
    contenido_csv = csv_handler.read_csv(file_path)
    csv_handler.write_csv(file_path, origen, fieldnames)
    # Mostrar el contenido del archivo CSV por pantalla
    print("Contenido del archivo CSV:")
    print(contenido_csv)
    
    # Leer archivo .json
    # json_handler = JSONFileHandler()
    # json_handler.write_json('libros_machado.json', 'libreria_origen', 'Ramón del Valle Inclán')
    # data = json_handler.read_json('libros_machado.json')
    # print("Contenido JSON")
    # print(data)

    # Ejecutar consulta SELECT para ver los datos insertados
    # cursor.execute("SELECT * FROM Libreria")

    # Insertar tabla en un .json
    # json_handler.write_json('inventario_final.json', )

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
