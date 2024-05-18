import psycopg2.pool
import sys
import yaml


# DECORADOR QUE CARGA LAS CREDENCIALES
def load_credentials_once(func):
    def wrapper(cls, *args, **kwargs):
        if not hasattr(cls, "__credentials_loaded"):
            with open("./config_files/db_config.yaml") as file:
                credentials = yaml.safe_load(file)

                cls.__USERNAME = credentials["database"]["username"]
                cls.__PASSWORD = credentials["database"]["password"]
                cls.__DB_PORT = credentials["database"]["port"]
                cls.__HOST = credentials["database"]["host"]
                cls.__credentials_loaded = True

        return func(cls, *args, **kwargs)
    return wrapper


class Connection:
    with open("./config_files/db_config.yaml") as file:
        credentials = yaml.safe_load(file)

    __DATABASE = credentials["database"]["database_name"]
    __USERNAME = credentials["database"]["username"]
    __PASSWORD = credentials["database"]["password"]
    __DB_PORT = credentials["database"]["port"]
    __HOST = credentials["database"]["host"]
    __MIN_CON = 1
    __MAX_CON = 5
    __pool = None



    # OBTENER POOL DE CONEXIONES
    @classmethod
    @load_credentials_once
    def getPool(cls):
        if cls.__pool is None:
            try:
                cls.__pool = psycopg2.pool.SimpleConnectionPool(
                    cls.__MIN_CON,
                    cls.__MAX_CON,
                    host=cls.__HOST,
                    user=cls.__USERNAME,
                    password=cls.__PASSWORD,
                    port=cls.__DB_PORT,
                    database=cls.__DATABASE
                )
                print("Creación pool exitosa:", cls.__pool)
                return cls.__pool
            except Exception as e:
                print("Error al crear el pool...", e)
                sys.exit()
        else:
            return cls.__pool

    # OBTENER CONEXION DEL POOL
    @classmethod
    @load_credentials_once
    def getConnection(cls):
        conn = cls.getPool().getconn()
        print("Conexión obtenida del pool: ", conn)
        return conn

    # LIBERAR LA CONEXIÓN
    @classmethod
    @load_credentials_once
    def releaseConnection(cls, conn):
        cls.getPool().putconn(conn)

    # CERRAR CONEXIONES
    @classmethod
    @load_credentials_once
    def closeConnections(cls):
        cls.getPool().closeall()
        print("Se han cerrado todas las conexiones del pool: ", cls.__pool)