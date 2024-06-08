from psycopg2 import Error
from models.productDAO import Product, ProductStock
from repositories import config_conn


# Lista todos los productos de la db
def mostrar_todos_productos():

    conn = None
    productos_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()

        cursor.execute("""SELECT * FROM public.producto""")
        productos = cursor.fetchall()

        for producto in productos:
            producto_obj = Product(
                code=producto[0],
                name=producto[1],
                price=producto[2],
                iva=producto[3],
                stock=producto[4]
            )
            productos_objetos.append(producto_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        return productos_objetos


# Consulta solo el stock de todos los productos de la db
def mostrar_stock():
    conn = None
    productos_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()

        cursor.execute("""SELECT codigo, nombre, stock FROM public.producto""")
        productos = cursor.fetchall()

        for producto in productos:
            producto_obj = ProductStock(
                code=producto[0],
                name=producto[1],
                stock=producto[2]
            )
            productos_objetos.append(producto_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        return productos_objetos


# Cosulta un producto por su código
def buscar_un_producto(codigo_producto):
    conn = None
    producto_obj = None
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()

        query = f"""SELECT * FROM public.producto WHERE codigo=%s"""
        params = (codigo_producto, )
        cursor.execute(query, params)
        productos = cursor.fetchall()

        for producto in productos:
            producto_obj = Product(
                code=producto[0],
                name=producto[1],
                price=producto[2],
                iva=producto[3],
                stock=producto[4]
            )

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        return producto_obj


# Insertar producto en la db
def insertar_producto(producto: Product):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        query = f"""INSERT INTO public.producto (nombre, precio, iva, stock) VALUES(%s, %s, %s, %s);"""
        params = (producto.name, producto.price, producto.iva, producto.stock)
        cursor.execute(query, params)
        conn.commit()
        mensaje = "Registro insertado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al insertar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        return mensaje


# Modifica todos los campos de un producto de la db (menos código)
def modificar_producto(producto: Product):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        query = f"""UPDATE public.producto SET nombre = %s, precio = %s, iva = %s, stock = %s WHERE codigo = %s;"""
        params = (producto.name, producto.price, producto.iva, producto.stock, producto.code)
        cursor.execute(query, params)
        conn.commit()
        mensaje = "Registro modificado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al modificar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        return mensaje


# Elimina producto de la db
def eliminar_producto(producto: Product):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        cursor = conn.cursor()
        query = f"""DELETE FROM public.producto WHERE codigo = %s;"""
        params = (producto.code, )
        cursor.execute(query, params)
        conn.commit()
        mensaje = "Registro eliminado con éxito"

    except Error as e:
        print(e)
        mensaje = "Se ha producido un error al eliminar el registro"

    finally:
        config_conn.Connection.releaseConnection(conn)
        return mensaje

