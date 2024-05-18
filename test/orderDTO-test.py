import pytest
from models.orderDTO import Order, OrderDTO

def test_order_creation():
    order = Order(1, 1)
    assert isinstance(order, Order), "El pedido debería ser una instancia de Order"
    assert order.code == 1, "El código del pedido debería ser 1"
    assert order.code_table == 1, "El código de la mesa debería ser 1"
    assert order.products == [], "Los productos del pedido deberían estar vacíos al inicio"

def test_add_product():
    order = Order(1, 1)
    product = {"producto1": 2}
    order.add_product(product)
    assert "producto1" in order.products[0], "El producto1 debería estar en los productos del pedido"
    assert order.products[0]["producto1"] == 2, "La cantidad del producto1 debería ser 2"

def test_delete_product():
    order = Order(1, 1)
    product = {"producto1": 2}
    order.add_product(product)
    order.delete_product(product)
    assert not order.products, "Los productos del pedido deberían estar vacíos después de eliminar el producto"

def test_to_OrderDTO():
    order = Order(1, 1)
    product = {"producto1": 2}
    order.add_product(product)
    order_dto = order.to_OrderDTO()
    assert order_dto.code == order.code, "El código del OrderDTO debería ser el mismo que el del Order"
    assert order_dto.code_table == order.code_table, "El código de la mesa del OrderDTO debería ser el mismo que el del Order"
    assert order_dto.products == order.products, "Los productos del OrderDTO deberían ser los mismos que los del Order"
