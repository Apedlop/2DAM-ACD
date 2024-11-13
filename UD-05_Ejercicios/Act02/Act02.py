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
    
    # Consultar los objetos que cumplan una condición
    print("Mostrar solo mascotas mayores de 2 años:")
    coleccion_usuarios = db["Mascotas"]
    consulta = {"edad": {"$gt": 2}}  # Filtrar usuarios con edad mayor a 2
    usuarios = coleccion_usuarios.find(consulta)
    for usuario in usuarios:
        print(usuario)
        
    # Mostrar campos específicos
    print("\nMostrar campos específicos:")
    proyeccion = {"nombre": 1, "edad": 1, "_id": 1}
    usuarios = coleccion_usuarios.find(consulta, proyeccion)
    for usuario in usuarios:
        print(usuario)
    
    # Limitar y ordenar los resultados mostrados
    print("\nCampos limitados y ordenados: ")
    usuarios = coleccion_usuarios.find(consulta).limit(2).sort("nombre", 1) # Usamos 1 para que sea ascendente
    for usuario in usuarios:
        print(usuario)
    
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