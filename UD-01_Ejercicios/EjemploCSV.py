import csv

class CSVFileHandler:
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

    def write_csv(self, file_path, data, fieldnames):
        try:
            with open(file_path, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)  # Creamos un objeto writer para escribir en CSV
                writer.writeheader()  # Escribimos la primera fila que contiene los nombres de las columnas (encabezado)
                writer.writerow(data)  # Escribimos los datos en una fila en el archivo CSV
        except Exception as e:
            print(f"Error escribiendo en el archivo CSV: {e}")

# Ejemplo de uso
csv_handler = CSVFileHandler()

# Definir la ruta del archivo CSV
file_path = 'data.csv'

# Datos para escribir en el archivo CSV (día, mes, año, DNI)
data = {
    "Día": "12",
    "Mes": "Junio",
    "Año": "1976",
    "DNI": "12345678"
}

# Definir los nombres de las columnas
fieldnames = ["Día", "Mes", "Año", "DNI"]

# Escribir los datos en el archivo CSV
csv_handler.write_csv(file_path, data, fieldnames)

# Leer los datos del archivo CSV
contenido_csv = csv_handler.read_csv(file_path)

# Mostrar el contenido del archivo CSV por pantalla
print("Contenido del archivo CSV:")
print(contenido_csv)
