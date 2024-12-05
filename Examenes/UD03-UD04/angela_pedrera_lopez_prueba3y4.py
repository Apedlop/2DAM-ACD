from peewee import MySQLDatabase, Model, CharField, IntegerField, PrimaryKeyField, IntegrityError
import ZODB, ZODB.FileStorage, transaction
from persistent import Persistent

# Configurar la base de datos
db = MySQLDatabase(
    '1dam',  # Nombre de la base de datos
    user='usuario',  # Usuario de MySQL
    password='usuario',  # Contraseña de MySQL
    host='localhost',  # Host
    port=3306  # Puerto de MySQL
)

try:
    # Conectar a la base de datos
    db.connect()
    print("Conexión exitosa a la base de datos.")

    # Definir la tabla 'Libros' con los campos especificados
    class Libros(Model):
        id = PrimaryKeyField(null=False)  
        titulo = CharField(max_length=100)  
        autor = CharField(max_length=100)  
        anio_publicacion = IntegerField(null=False)  
        genero = CharField(max_length=50) 

        class Meta:
            database = db
            table_name = 'Libros'

    # Definir clase ZODB Prestamos
    class Prestamos(Persistent):
        def __init__(self, libro_id, nombre_usuario, fecha_prestamo, fecha_devolucion):
            self.libro_id = libro_id
            self.nombre_usuario = nombre_usuario
            self.fecha_prestamo = fecha_prestamo
            self.fecha_devolucion = fecha_devolucion

    # Función para verificar si la tabla existe
    def tabla_existe(nombre_tabla):
        consulta = """SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"""
        cursor = db.execute_sql(consulta, ('1dam', nombre_tabla))
        resultado = cursor.fetchone()
        return resultado[0] > 0

    # Eliminar la tabla si ya existe
    if tabla_existe(Libros._meta.table_name):
        print(f"La tabla '{Libros._meta.table_name}' existe.")
        db.drop_tables([Libros], cascade=True)
        print(f"Tabla '{Libros._meta.table_name}' eliminada con éxito.")
    else:
        print(f"La tabla '{Libros._meta.table_name}' no existe.")

    # Crear la tabla 'Libros'
    db.create_tables([Libros])
    print("Tabla 'Libros' creada o ya existente.")

    # Iniciar una transacción para insertar registros
    try:
        # Usar db.atomic() para asegurar la transacción, si ocurre algún error se deshacen los cambios
        with db.atomic():
            
            libros = [
                {'titulo': 'Cien años de soledad', 'autor': 'Gabriel García Márquez', 'anio_publicacion': 1967, 'genero': 'Novela'}, 
                {'titulo': 'Don Quijote de la Mancha', 'autor': 'Miguel de Cervantes', 'anio_publicacion': 1605, 'genero': 'Novela'},
                {'titulo': 'El Principito', 'autor': 'Antoine de Saint-Exupéry', 'anio_publicacion': 1943, 'genero': 'Infantil'},
                {'titulo': 'Crónica de una muerte anunciada', 'autor': 'Gabriel García Márquez', 'anio_publicacion': 1981, 'genero': 'Novela'},
                {'titulo': '1984', 'autor': 'George Orwell', 'anio_publicacion': 1949, 'genero': 'Distopía'}
            ]
            
            Libros.insert_many(libros).execute()
          
            print("Registros insertados en la tabla 'Libros' con éxito.")
    except IntegrityError as e:
        # Manejar el error en caso de que ocurra
        print(f"Error al insertar registros en la tabla 'Libros': {e}")

      # Establecer conexión
    try :
        storage = ZODB.FileStorage.FileStorage('1dam.fs')
        db = ZODB.DB(storage)
        connection = db.open()
        root = connection.root()

        try :
            def buscar_prestamo(genero_libro):
                if 'libros' not in root:
                    root['libros'] = {}
                
                librosMysql = Libros.select()
                
                for libro in librosMysql:
                    zodb_libro = Libros(libro.id, libro.titulo, libro.autor, libro.anio_publicacion, libro.genero)
                    root['libros']['libros'] = zodb_libro
                
                for libro in root['libros'].values():
                    if libro.genero == genero_libro:
                        print(f"{libro.id}, {libro.titulo}, {libro.autor}, {libro.genero}")
                        prestamos = root['prestamo'].values
                        if prestamos.libro_id == libro.id:
                            print(f"{prestamos.id}, {prestamos.genero}, {prestamos.nombre_usuarios}")
            buscar_prestamo('Novela')
        except Exception:
            print("Hubo un error al listar el genero")      
                
        if 'prestamo' not in root:
            root['prestamo'] = {}
            transaction.commit

        # Almacenar una prestamo
        root['prestamo']['prestamo1'] = Prestamos(1, 'Juan Perez', '2023-10-01', '2023-11-01')
        root['prestamo']['prestamo2'] = Prestamos(2, 'Ana Lopez', '2023-09-15', '2023-10-15')
        root['prestamo']['prestamo3'] = Prestamos(4, 'Maria Gomez', '2023-09-20', '2023-10-20')

        # Guardar cambios en la base de datos
        transaction.commit()

        # Filtrar prestamos por nombre de usuario
        for clave, prestamo in root.items():
            if hasattr(prestamo, 'nombre_usuario'):
                print(f"Tipo: {prestamo.nombre_usuario}")

    except Exception:
        print("Hubo un error al insertar los Prestamos")
        
    # Cerrar la conexión a la base de datos
    connection.close()
    db.close()
    print("Conexión cerrada.")
except Exception:
    print("Hubo un error al conectar con la base de datos.")