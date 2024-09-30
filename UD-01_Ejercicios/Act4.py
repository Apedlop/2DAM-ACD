import csv
import json

class FileConverter:
    def csv_to_json(self, csv_file, json_file):
        try:
            with open(json_file, 'r') as f:
                reader = json.load(f)
                rows = list(reader)
                clave = list(reader.keys()) # Sacamos las claves de la lista
            with open(csv_file, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=clave)
                writer.writeheader()
                writer.writerow(reader)
            print(f'Conversión de {json_file} a {csv_file} completada.')
        except Exception as e:
            print(f"Error en la conversión: {e}")

# Uso
converter = FileConverter()
converter.csv_to_json('data.csv', 'data.json')
