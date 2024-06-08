from psycopg2 import Error
from models.tableDAO import Table
from repositories import config_conn


# Lista todas las mesas de la db
def mostrar_todas_mesas():
    conn = None
    mesas_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM public.mesa""")
        mesas = cursor.fetchall()

        for mesa in mesas:
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
        return mesas_objetos


# Consulta las mesas y las reservas asociadas (JOIN)
def mostrar_mesas_reserva():
    conn = None
    mesas_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        cursor.execute("""SELECT m.*, COALESCE(r.fecha, NULL) AS fecha
                        FROM public.mesa m
                        LEFT JOIN (
                            SELECT mesa_codigo, fecha
                            FROM public.reserva
                            WHERE fecha >= CURRENT_DATE
                        ) r ON m.codigo = r.mesa_codigo
                        ORDER BY m.codigo;""")
        mesas = cursor.fetchall()

        for mesa in mesas:
            if mesa[3]:
                mesa_obj = Table(
                    code=mesa[2],
                    name=mesa[0],
                    state="Próxima reserva " + str(mesa[3])
                )
            else:
                mesa_obj = Table(
                    code=mesa[2],
                    name=mesa[0],
                    state="Sin reservas"
                )
            mesas_objetos.append(mesa_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        return mesas_objetos


# Busca una mesa en la db por el código
def buscar_mesa(codigo_mesa: int):
    conn = None
    mesas_objetos = []
    mesa_obj = None
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        query = f"""SELECT * FROM public.mesa WHERE codigo=%s"""
        params = (codigo_mesa, )
        cursor.execute(query, params)
        mesas = cursor.fetchall()

        for mesa in mesas:
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
        return mesa_obj


# Inserta mesa en la db
def insertar_mesa(mesa: Table):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        query = f"""INSERT INTO public.mesa (nombre, estado) VALUES(%s, %s);"""
        params = (mesa.name, mesa.state)
        cursor.execute(query, params)
        conn.commit()
        mensaje = "Registro insertado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al insertar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        return mensaje


# Modifica los campos nombre y estado de una mesa en la db
def modificar_mesa(mesa: Table):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        query = f"""UPDATE public.mesa SET nombre = %s, estado = %s WHERE codigo = %s;"""
        params = (mesa.name, mesa.state, mesa.code)
        cursor.execute(query, params)
        conn.commit()
        mensaje = "Registro modificado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al modificar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        return mensaje

# Elimina una mesa de la db
def eliminar_mesa(mesa: Table):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        query = f"""DELETE FROM public.mesa WHERE codigo = %s;"""
        params = (mesa.code, )
        cursor.execute(query, params)
        conn.commit()
        mensaje = "Registro eliminado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al eliminar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        return mensaje




