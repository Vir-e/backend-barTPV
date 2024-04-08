from pydantic import BaseModel


class Product(BaseModel):
    code: int | None
    name: str | None
    price: float | None
    iva: int | None
    stock: int | None


class ProductStock(BaseModel):
    code: int | None = None
    name: str | None = None
    stock: int | None = None

