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
        cursor.execute(f"""INSERT INTO public.reserva (mesa_codigo, fecha, num_personas, nota) VALUES({reserva.table_code}, '{reserva.date}', '{reserva.num_people}', '{reserva.note}');""")
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
        cursor.execute(f"""SELECT * FROM public.reserva WHERE codigo={codigo_reserva}""")
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
        cursor.execute(f"""DELETE FROM public.reserva WHERE codigo = {reserva.code};""")
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
        cursor.execute(f"""UPDATE public.reserva SET mesa_codigo = {reserva.table_code}, fecha = '{reserva.date}', num_personas = {reserva.num_people}, nota = '{reserva.note}' WHERE codigo = {reserva.code};""")
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

