import json
import csv
import os
import logging
from datetime import datetime

# Configuración de logging para guardar en un archivo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("log_datos.log")]
)

class DataManager:
    def __init__(self, archivo, tipo_archivo):
        self.archivo = archivo
        self.tipo_archivo = tipo_archivo
        self.transaccion = None
        self.log = logging.getLogger(__name__)

    def _obtener_datos(self):
        if self.tipo_archivo == 'json':
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    try:
                        return json.load(f)
                    except json.JSONDecodeError:
                        self.log.warning("El archivo JSON está vacío o tiene un formato incorrecto.")
                        return []
            return []
        elif self.tipo_archivo == 'csv':
            if os.path.exists(self.archivo):
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    lector = csv.DictReader(f)
                    if lector.fieldnames:
                        return [row for row in lector]
                    else:
                        self.log.warning("El archivo CSV está vacío.")
                        return []
            return []
        else:
            raise ValueError("Tipo de archivo no soportado.")

    def _guardar_datos(self, datos):
        """Guardar los datos en el archivo."""
        if self.tipo_archivo == 'json':
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
        elif self.tipo_archivo == 'csv':
            if datos:
                fieldnames = datos[0].keys()
                with open(self.archivo, 'w', encoding='utf-8', newline='') as f:
                    escritor = csv.DictWriter(f, fieldnames=fieldnames)
                    escritor.writeheader()
                    escritor.writerows(datos)
            else:
                self.log.warning("No hay datos para guardar en el archivo CSV.")
        else:
            raise ValueError("Tipo de archivo no soportado.")

    def iniciar_transaccion(self):
        """Inicia una transacción para guardar datos de manera controlada."""
        self.transaccion = self._obtener_datos()
        self.log.info(f"Transacción iniciada en {datetime.now()}")

    def escribir_dato(self, dato):
        """Escribe un nuevo dato en la transacción."""
        if self.transaccion is None:
            raise ValueError("Transacción no iniciada.")
        self.transaccion.append(dato)
        self.log.info(f"Dato escrito: {dato}")

    def confirmar_transaccion(self):
        """Confirma la transacción y guarda los datos."""
        if self.transaccion is None:
            raise ValueError("Transacción no iniciada.")
        self._guardar_datos(self.transaccion)
        self.transaccion = None
        self.log.info(f"Transacción confirmada y datos guardados en {datetime.now()}")

    def revertir_transaccion(self):
        """Revierte la transacción."""
        self.transaccion = None
        self.log.info(f"Transacción revertida en {datetime.now()}")


class Mascota:
    def __init__(self, tipo, raza, edad, peso, nombre):
        self.tipo = tipo
        self.raza = raza
        self.edad = edad
        self.peso = peso
        self.nombre = nombre

    def to_dict(self):
        """Convierte la instancia de Mascota a un diccionario."""
        return {
            'tipo': self.tipo,
            'raza': self.raza,
            'edad': self.edad,
            'peso': self.peso,
            'nombre': self.nombre
        }


# Instanciar tres objetos de la clase Mascota
mascota1 = Mascota("Perro", "Bodeguero", 3, 9.8, "Yoyo")
mascota2 = Mascota("Gato", "Persa", 3, 4.5, "Luna")
mascota3 = Mascota("Conejo", "Mini Lop", 2, 2.2, "Bolita")

# Crear una lista con las instancias
mascotas = [mascota1, mascota2, mascota3]

# Crear una instancia de DataManager para trabajar con JSON
data_manager_json = DataManager('mascotas.json', 'json')

# Iniciar una transacción
data_manager_json.iniciar_transaccion()

# Escribir las instancias en el archivo JSON
for mascota in mascotas:
    data_manager_json.escribir_dato(mascota.to_dict())

# Confirmar la transacción y guardar el archivo JSON
data_manager_json.confirmar_transaccion()

# Cambiar a formato CSV
data_manager_csv = DataManager('mascotas.csv', 'csv')

# Iniciar una nueva transacción para CSV
data_manager_csv.iniciar_transaccion()

# Escribir las mismas instancias en el archivo CSV
for mascota in mascotas:
    data_manager_csv.escribir_dato(mascota.to_dict())

# Confirmar la transacción y guardar el archivo CSV
data_manager_csv.confirmar_transaccion()
