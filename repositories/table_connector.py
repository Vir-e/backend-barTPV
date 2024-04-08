from psycopg2 import Error
from models.tableDAO import Table
from repositories import config_conn
'''
host = "localhost"
dbname = "db_gestionempresa"
user = "postgres"
password = "root"


conn = None
cursor = None
try:
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port="5432")
    print("Conexión abierta")

    cursor = conn.cursor()
    result = cursor.execute("""INSERT INTO public.cliente VALUES(3, 'Jose Rueda Lorenzo', 'C/ Panaderas 14', '6948630', 'joserueda@gmail.com', '49628850P')""")
    print(result)
    conn.commit()

    print("Registro insertado con éxito")

    result = cursor.execute("""SELECT * FROM cliente""")
    print(result)

    print("Registro leido")

except Exception as ex:
    print(ex)

finally:
    cursor.close()
    conn.close()
    print("Conexión cerrada")


#FUNCIONA CONECTANDO CON PSYCOP2 SIN POOL, COGIENDO CREDENCIALES DEL YAML
def cargar_credenciales():
    with open("/config_files/db_config.yaml", 'r') as archivo:
        credenciales = yaml.safe_load(archivo)
    return credenciales
'''


def mostrar_todas_mesas():
    conn = None
    mesas_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")

        cursor = conn.cursor()

        print("Registros leidos:")
        cursor.execute("""SELECT * FROM public.mesa""")
        mesas = cursor.fetchall()

        for mesa in mesas:
            print(mesa)
            mesa_obj = Table(
                code=mesa[2],
                name=mesa[0],
                state=mesa[1]
            )
            mesas_objetos.append(mesa_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        print("Conexión cerrada")
        return mesas_objetos


def buscar_mesa(codigo_mesa: int):
    conn = None
    mesas_objetos = []
    mesa_obj = None
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")

        cursor = conn.cursor()

        print("Registros leidos:")
        cursor.execute(f"""SELECT * FROM public.mesa WHERE codigo={codigo_mesa}""")
        mesas = cursor.fetchall()

        for mesa in mesas:
            print(mesa)
            mesa_obj = Table(
                code=mesa[2],
                name=mesa[0],
                state=mesa[1]
            )
            mesas_objetos.append(mesa_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        print("Conexión cerrada")
        return mesa_obj


def insertar_mesa(mesa: Table):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")
        print(mesa)
        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO public.mesa (nombre, estado) VALUES('{mesa.name}', '{mesa.state}');""")
        conn.commit()
        print("El registro se ha insertado exitosamente")
        mensaje = "Registro insertado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al insertar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        print("Conexión cerrada")
        return mensaje


def modificar_estado_mesa(mesa: Table):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")
        print(mesa)
        cursor = conn.cursor()
        cursor.execute(f"""UPDATE public.mesa SET estado = '{mesa.state}' WHERE codigo = {mesa.code};""")
        conn.commit()
        print("El registro se ha modificado exitosamente")
        mensaje = "Registro modificado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al modificar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        print("Conexión cerrada")
        return mensaje


'''
def ejemploBORRAR():
    conn = config_conn.Connection.getConnection()
    print("Ha recibido la conexion")
    config_conn.Connection.releaseConnection(conn)
    print("Ha liberado la conexión")
    config_conn.Connection.closeConnections()
    print("Se ha cerrado el pool")
'''

#buscar_mesa(12)


def eliminar_mesa(mesa: Table):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")
        print(mesa)
        cursor = conn.cursor()
        cursor.execute(f"""DELETE FROM public.mesa WHERE codigo = {mesa.code};""")
        conn.commit()
        print("El registro se ha eliminado exitosamente")
        mensaje = "Registro eliminado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al eliminar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        print("Conexión cerrada")
        return mensaje




