from pydantic import BaseModel


# obj BaseModel para ser mandado en la respuesta de peticiones
class OrderDTO(BaseModel):
    code: int
    code_table: int
    products: list[dict]


# CLASE PEDIDO CON LAS FUNCIONALIDADES DE AGREGAR Y ELIMINAR PRODUCTOS
class Order:
    def __init__(self, code: int, code_table: int):
        self.code = code
        self.code_table = code_table
        self.products = []

    def to_dict(self):
        return {
            "cod_pedido": self.code,
            "cod_mesa": self.code_table,
            "productos": self.products
        }

    def add_product(self, product: dict):
        self.products.append(product)

    def delete_product(self, product: dict):
        self.products.remove(product)

    # Convertir a obj BaseModel
    def to_OrderDTO(self):
        return OrderDTO(
            code=self.code,
            code_table=self.code_table,
            products=self.products
        )
