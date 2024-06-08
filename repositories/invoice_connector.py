import json
from psycopg2 import Error
from models.invoiceDAO import Invoice
from repositories import config_conn


# Lista todas las facturas de la db
def mostrar_todas_facturas():

    conn = None
    facturas_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM public.factura""")
        facturas = cursor.fetchall()

        for factura in facturas:
            factura_obj = Invoice(
                code=factura[0],
                code_table=factura[1],
                date=factura[5],
                concept=factura[6],
                total_gross_amount=factura[2],
                iva_applied=factura[3],
                total_invoice=factura[4]
            )
            facturas_objetos.append(factura_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        return facturas_objetos


# Devuelve factura de la db por su código
def buscar_factura(codigo_fac: int):
    conn = None
    facturas_objetos = []
    factura_obj = None
    try:
        conn = config_conn.Connection.getConnection()

        cursor = conn.cursor()

        query = f"""SELECT * FROM public.factura WHERE codigo=%s"""
        params = (codigo_fac, )
        cursor.execute(query, params)
        facturas = cursor.fetchall()

        for factura in facturas:
            factura_obj = Invoice(
                code=factura[0],
                code_table=factura[1],
                date=factura[5],
                concept=factura[6],
                total_gross_amount=factura[2],
                iva_applied=factura[3],
                total_invoice=factura[4]
            )
            facturas_objetos.append(factura_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        return factura_obj


# Devuelve el código de la última factura
def buscar_ultima_factura():
    conn = None
    n_ult_factura = 0
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()

        cursor.execute(f"""SELECT * FROM public.factura WHERE codigo = (SELECT MAX(codigo) FROM public.factura);""")
        facturas = cursor.fetchall()

        for factura in facturas:
            factura_obj = Invoice(
                code=factura[0],
                code_table=factura[1],
                concept=factura[6],
                total_gross_amount=factura[2],
                iva_applied=factura[3],
                total_invoice=factura[4],
                date=factura[5]
            )
            n_ult_factura = factura_obj.code
    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        return n_ult_factura


# Inserta una factura en la db
def insertar_factura(factura: Invoice):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        query = f"""INSERT INTO public.factura (codigo, mesa_cod, concepto, importe_bruto, iva_aplicado, importe_neto, fecha) VALUES(%s, %s, %s, %s, %s, %s, %s);"""
        params = (factura.code, factura.code_table, (json.dumps(factura.concept)), factura.total_gross_amount, factura.iva_applied, factura.total_invoice, factura.date)

        cursor.execute(query, params)
        conn.commit()
        mensaje = "Registro insertado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al insertar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        return mensaje


# Eliminar factura de la db
def eliminar_factura(factura: Invoice):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        query = f"""DELETE FROM public.factura WHERE codigo = %s;"""
        params = (factura.code, )
        cursor.execute(query, params)
        conn.commit()
        mensaje = "Registro eliminado con éxito"

    except Error as e:
        mensaje = "Se ha producido un error al eliminar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        return mensaje
