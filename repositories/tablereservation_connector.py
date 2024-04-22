from psycopg2 import Error
from models.table_reservationDAO import TableReservation
from repositories import config_conn


def insertar_reserva(reserva: TableReservation):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")
        print(reserva)
        cursor = conn.cursor()
        query = f"""INSERT INTO public.reserva (mesa_codigo, fecha, num_personas, nota) VALUES(%s, %s, %s, %s);"""
        params = (reserva.table_code, reserva.date, reserva.num_people, reserva.note)
        cursor.execute(query, params)
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


def mostrar_todas_reservas():
    conn = None
    reservas_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")

        cursor = conn.cursor()

        print("Registros leidos:")
        cursor.execute("""SELECT * FROM public.reserva""")
        reservas = cursor.fetchall()

        for reserva in reservas:
            print(reserva)
            reserva_obj = TableReservation(
                code=reserva[0],
                table_code=reserva[1],
                date=reserva[2],
                num_people=reserva[3],
                note=reserva[4]
            )
            reservas_objetos.append(reserva_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        print("Conexión cerrada")
        return reservas_objetos


def buscar_reserva(codigo_reserva: int):
    conn = None
    reserva_obj = None
    reservas_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")

        cursor = conn.cursor()

        print("Registros leidos:")
        query = f"""SELECT * FROM public.reserva WHERE codigo=%s"""
        params = (codigo_reserva, )
        cursor.execute(query, params)
        reservas = cursor.fetchall()

        for reserva in reservas:
            print(reserva)
            reserva_obj = TableReservation(
                code=reserva[0],
                table_code=reserva[1],
                date=reserva[2],
                num_people=reserva[3],
                note=reserva[4]
            )
            reservas_objetos.append(reserva_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        print("Conexión cerrada")
        return reserva_obj


def eliminar_reserva(reserva: TableReservation):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")
        print(reserva)
        cursor = conn.cursor()
        query = f"""DELETE FROM public.reserva WHERE codigo = %s;"""
        params = (reserva.code, )
        cursor.execute(query, params)
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


def modificar_reserva(reserva: TableReservation):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")
        print(reserva)
        cursor = conn.cursor()
        query = f"""UPDATE public.reserva SET mesa_codigo = %s, fecha = %s, num_personas = %s, nota = %s WHERE codigo = %s;"""
        params = (reserva.table_code, reserva.date, reserva.num_people, reserva.note, reserva.code)
        cursor.execute(query, params)
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

