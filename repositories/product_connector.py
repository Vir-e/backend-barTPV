from psycopg2 import Error
from models.productDAO import Product, ProductStock
from repositories import config_conn


def mostrar_todos_productos():

    conn = None
    productos_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")

        cursor = conn.cursor()

        print("Registros leidos:")
        cursor.execute("""SELECT * FROM public.producto""")
        productos = cursor.fetchall()

        for producto in productos:
            print(producto)
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
        print("Conexión cerrada")
        return productos_objetos


def mostrar_stock():
    conn = None
    productos_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")

        cursor = conn.cursor()

        print("Registros leidos:")
        cursor.execute("""SELECT codigo, nombre, stock FROM public.producto""")
        productos = cursor.fetchall()

        for producto in productos:
            print(producto)
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
        print("Conexión cerrada")
        return productos_objetos


def buscar_un_producto(codigo_producto):
    conn = None
    producto_obj = None
    #productos_objetos = []
    try:
        conn = config_conn.Connection.getConnection()
        #print("Conexión abierta")

        cursor = conn.cursor()

        #print("Registros leidos:")
        cursor.execute(f"""SELECT * FROM public.producto WHERE codigo={codigo_producto}""")
        productos = cursor.fetchall()

        for producto in productos:
            #print(producto)
            producto_obj = Product(
                code=producto[0],
                name=producto[1],
                price=producto[2],
                iva=producto[3],
                stock=producto[4]
            )
            #productos_objetos.append(producto_obj)

    except Error as e:
        print(e)
    except Exception as ex:
        print(ex)

    finally:
        config_conn.Connection.releaseConnection(conn)
        #print("Conexión cerrada")
        return producto_obj


def insertar_producto(producto: Product):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")
        print(producto)
        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO public.producto (nombre, precio, iva, stock) VALUES('{producto.name}', {producto.price}, {producto.iva}, {producto.stock});""")
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


def modificar_producto(producto: Product):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")
        print(producto)
        cursor = conn.cursor()
        cursor.execute(f"""UPDATE public.producto SET nombre = '{producto.name}', precio = {producto.price}, iva = {producto.iva}, stock = {producto.stock} WHERE codigo = {producto.code};""")
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


def eliminar_producto(producto: Product):
    conn = None
    mensaje = ""
    try:
        conn = config_conn.Connection.getConnection()
        print("Conexión abierta")
        print(producto)
        cursor = conn.cursor()
        cursor.execute(f"""DELETE FROM public.producto WHERE codigo = {producto.code};""")
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

