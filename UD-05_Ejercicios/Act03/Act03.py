from pymongo import MongoClient, errors

# Datos de conexión
usuario = "usuario"
clave = "usuario"
base_datos = "1dam"
host = "localhost"
puerto = 27017

try:
    # Intentar conectarse al servidor MongoDB
    client = MongoClient(f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}", serverSelectionTimeoutMS=5000)
    
    # Seleccionar la base de datos
    db = client[base_datos]
    
    # Intentar acceder a la base de datos para verificar la conexión
    colecciones = db.list_collection_names()
    
    print("Conexión exitosa. Colecciones en la base de datos:")
    print(colecciones)
    
    # Seleccionar o crear la colección 'mascotas'
    coleccion_mascotas = db["Mascotas"]
    
    print("Añadir múltiples documentos:")
    
    # Añadir múltiples documentos a la colección
    nueva_mascota = [
        {"_id": 7, "tipo": "Conejo", "raza": "Mini Lop", "edad": 2, "peso": 2.5, "nombre": "colita"},
        {"_id": 8, "tipo": "Tortuga", "raza": "Hermann", "edad": 6, "peso": 1.2, "nombre": "Shelly"},
        {"_id": 9, "tipo": "Hamster", "raza": "Siberiano", "edad": 1, "peso": 0.2, "nombre": "Nibbles"}
    ]
    añadir = coleccion_mascotas.insert_many(nueva_mascota)
    print("Documentos insertados con los siguientes _id:")
    print(añadir.inserted_ids)
    
    print("\nActualiar un campo de un documento:")
    
    # Actualizar un campo de un sólo documento
    actualizar = coleccion_mascotas.update_one(
        {"nombre": "Patitas"}, # Filtro para encontrar el documento
        {"$set": {"Raza": "Siamés"}} # Campos que quiero modificar
    )
    print(f"Documento modificado: {actualizar.modified_count}")
    
    print("\nEliminar un documento:")
    
    # Eliminar un solo documento
    eliminar = coleccion_mascotas.delete_one({"nombre": "Max"})
    #Verificar si el documento fue eliminado
    if eliminar.deleted_count > 0:
        print("Documento eliminado con éxito.")
    else:
        print("No se encontró el documento para eliminar.")
            
except errors.ServerSelectionTimeoutError as err:
    # Este error ocurre si el servidor no está disponible o no se puede conectar
    print(f"No se pudo conectar a MongoDB: {err}")
    
except errors.OperationFailure as err:
    # Este error ocurre si las credenciales son incorrectas o no se tienen los permisos necesarios
    print(f"Fallo en la autenticación o permisos insuficientes: {err}")

except Exception as err:
    # Manejar cualquier otro error inesperado
    print(f"Ocurrió un error inesperado: {err}")
    
finally:
    # Cerrar la conexión si se estableció correctamente
    if 'client' in locals():
        client.close()
        print("Conexión cerrada.")
