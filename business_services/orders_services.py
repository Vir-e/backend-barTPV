from pydantic import ValidationError
from repositories.product_connector import buscar_un_producto
from repositories.invoice_connector import buscar_ultima_factura, insertar_factura
from models.orderDTO import Order
from models.invoiceDAO import Invoice
from datetime import datetime
from globals import listado_pedidos_actuales


# Crear un pedido vacío
def iniciar_pedido(cod_mesa: int):
    n_ult_fact = buscar_ultima_factura()
    n_ult_pedido = 0
    if listado_pedidos_actuales:
        maximo = listado_pedidos_actuales[0]
        for pedido in listado_pedidos_actuales:
            if pedido.code > maximo.code:
                maximo = pedido
        n_ult_pedido = maximo.code

    if n_ult_fact >= n_ult_pedido:
        n_pedido = n_ult_fact + 1
    else:
        n_pedido = n_ult_pedido + 1
    pedido = Order(
        code=n_pedido,
        code_table=cod_mesa,
    )
    return pedido


# Añade producto y cantidad a un pedido
def agregar_al_pedido(pedido: Order, producto_cantidad: dict):
    pedido.add_product(producto_cantidad)
    return pedido


# Elimina un producto y su cantidad de un pedido
def eliminar_del_pedido(pedido: Order, producto_cantidad: dict):
    pedido.delete_product(producto_cantidad)
    return pedido


# Mostrar descripción del pedido
def mostrar_descripcion_pedido(pedido: Order):
    for p in pedido.products:
        print(p)
        for clave in p.keys():
            print(clave)
            producto = buscar_un_producto(clave)
            print(producto)
        print()


# Genera factura de un pedido
def generar_factura(pedido: Order):
    importes_brutos = []
    importes_iva = []
    suma_ivas = []
    lineas_productos = []
    for p in pedido.products:
        for producto_cod, cantidad in p.items():
            producto = buscar_un_producto(producto_cod)
            precio_total_producto = producto.price * cantidad
            importes_brutos.append(precio_total_producto)
            iva = producto.iva / 100
            valor_iva = producto.price * iva
            suma_ivas.append(valor_iva)
            precio_final = (producto.price + valor_iva) * cantidad
            importes_iva.append(precio_final)
            linea = {
                "codigo_producto": producto.code,
                "nombre_producto": producto.name,
                "iva_producto": producto.iva,
                "precio_unitario": producto.price,
                "cantidad": cantidad,
                "total_bruto": precio_total_producto,
                "total_neto": precio_final
            }

            lineas_productos.append(linea)
    total_bruto = sum(importes_brutos)
    total_factura = sum(importes_iva)
    iva_aplicado = sum(suma_ivas)
    factura = None
    fecha_completa = str(datetime.now())
    fecha = fecha_completa.split(".")[0]
    try:
        factura = Invoice(
            code=pedido.code,
            date=fecha,
            code_table=pedido.code_table,
            concept=lineas_productos,
            total_gross_amount=total_bruto,
            iva_applied=iva_aplicado,
            total_invoice=total_factura
        )
    except ValidationError as ex:
        print(repr(ex.errors()[0]['type']))

    insertar_factura(factura)
    return factura




