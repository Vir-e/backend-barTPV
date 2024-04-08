from models.orderDTO import Order
from models.productDAO import Product
from repositories.invoice_connector import buscar_ultima_factura
from repositories.tablereservation_connector import mostrar_todas_reservas
from business_services import orders_services

'''
def pedido():
    producto1 = Product(
        code=1,
        name="Fanta",
        description="",
        price=2.4,
        iva=21,
        stock=200
    )

    producto2 = Product(
        code=2,
        name="Jamón",
        description="",
        price=12.9,
        iva=21,
        stock=5
    )

    # creacion pedido vacio para una mesa
    n_pedido = buscar_ultima_factura() + 1

    pedido = Order(n_pedido, 12)

    # Productos solicitados por los clientes
    solicitud_clientes = []
    clave = producto1.code
    dic_prod = {clave: 5}
    solicitud_clientes.append(dic_prod)
    solicitud_clientes.append({producto2.code: 2})

    print("solicitud_clientes")
    print(solicitud_clientes)

    if len(solicitud_clientes) > 0:
        for diccionario_producto in solicitud_clientes:
            pedido.add_product(diccionario_producto)

    print("pedido", pedido)
    print(pedido.code)
    print(pedido.code_table)
    print(pedido.products)

pedido()

'''

def mostrar_reservas():
    reservas = mostrar_todas_reservas()
    return reservas