import json

class JSONFileHandler:
    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo JSON: {e}")

    def write_json(self, file_path, dni, fecha):
        try:
            with open(file_path, 'w') as f:
                data = {} # Creamos un diccionario vacío
                data["DNI"] = dni # Añadimos al Strign DNI el valor dni
                data["Fecha_Nacimiento"] = fecha # Añadimos al String Fecha_Nac el valor fecha
                json.dump(data, f) # Para crear y/o guardar en el fichero
                return data
        except Exception as e:
            print(f"Error leyendo JSON: {e}")
            
# Uso
json_handler = JSONFileHandler()
json_handler.write_json('data.json', '4042', '10/01/2005')
data = json_handler.read_json('data.json')
print(data)
