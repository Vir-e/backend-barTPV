import pytest
from models.orderDTO import Order
from business_services.orders_services import iniciar_pedido, agregar_al_pedido, eliminar_del_pedido, generar_factura

def test_iniciar_pedido():
    pedido = iniciar_pedido(1)
    assert pedido.code == 11
    assert pedido.code_table == 1
    assert pedido.products == []

def test_agregar_al_pedido():
    pedido = Order(code=1, code_table=1)
    producto_cantidad = {"producto1": 2}
    pedido = agregar_al_pedido(pedido, producto_cantidad)
    assert pedido.products == [producto_cantidad]

def test_eliminar_del_pedido():
    pedido = Order(code=1, code_table=1)
    producto_cantidad = {"producto1": 2}
    pedido.add_product(producto_cantidad)
    pedido = eliminar_del_pedido(pedido, producto_cantidad)
    assert pedido.products == []

def test_generar_factura():
    # Crear un pedido con productos
    pedido = Order(code=11, code_table=19)
    producto_cantidad = {"producto1": 2}
    pedido = agregar_al_pedido(pedido, producto_cantidad)

    # Generar la factura
    factura = generar_factura(pedido)

    # Comprobar que la factura se ha generado correctamente
    assert factura.code == pedido.code
    assert factura.code_table == pedido.code_table
    assert factura.total_gross_amount == 2 * 2
    assert factura.total_invoice == (2 + 2 * 21 / 100) * 2

