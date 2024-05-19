from fastapi import FastAPI, Form, HTTPException, Body
#from fastapi.responses import HTMLResponse, FileResponse
from typing import Annotated
from globals import listado_pedidos_actuales
from fastapi.params import Body
from models.tableDAO import Table
from models.productDAO import Product
from models.table_reservationDAO import TableReservation
from fastapi.staticfiles import StaticFiles
from business_services.orders_services import iniciar_pedido, agregar_al_pedido, eliminar_del_pedido, generar_factura
from repositories import product_connector, tablereservation_connector, table_connector, invoice_connector

# para evitar problema cors por origen
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.mount("/static_BORRAR", StaticFiles(directory="static_BORRAR"), name="static_BORRAR")

# Origenes permitidos para hacer peticiones
origins = [
    "http://localhost:63342",
    "http://localhost:9000",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
]
# config de las cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"Hello": "World"}


# ENDPOINTS HTML
'''
@app.get("/home", response_class=HTMLResponse)
async def home():
    html_content = ""
    # Abre el archivo HTML en modo lectura
    with open('static_BORRAR/html/gestion_index.html', 'r', encoding='utf-8') as archivo:
        # Lee el contenido del archivo
        html_content = archivo.read()

    # Imprime el contenido del archivo
    print(html_content)
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/table_form", response_class=HTMLResponse)
async def table_form():
    html_content = ""
    # Abre el archivo HTML en modo lectura
    with open('static_BORRAR/html/formulario_mesas.html', 'r', encoding='utf-8') as archivo:
        # Lee el contenido del archivo
        html_content = archivo.read()

    # Imprime el contenido del archivo
    print(html_content)
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/product_form", response_class=HTMLResponse)
async def product_form():
    html_content = ""
    # Abre el archivo HTML en modo lectura
    with open('static_BORRAR/html/formulario_productos.html', 'r', encoding='utf-8') as archivo:
        # Lee el contenido del archivo
        html_content = archivo.read()

    # Imprime el contenido del archivo
    print(html_content)
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/tables_view", response_class=HTMLResponse)
async def tables_view():
    html_address = "static_BORRAR/html/vista_mesas.html"
    return FileResponse(html_address, status_code=200)


@app.get("/products_view", response_class=HTMLResponse)
async def products_view():
    html_address = "static_BORRAR/html/prueba02.html"
    return FileResponse(html_address, status_code=200)


@app.get("/delivery_form", response_class=HTMLResponse)
async def delivery_form():
    html_content = ""
    # Abre el archivo HTML en modo lectura
    with open('static_BORRAR/html/prueba.html', 'r', encoding='utf-8') as archivo:
        # Lee el contenido del archivo
        html_content = archivo.read()

    # Imprime el contenido del archivo
    print(html_content)
    return HTMLResponse(content=html_content, status_code=200)
'''

########## api ###########


# GET
@app.get("/bar/api/v1/reservas")
async def get_reservas():
    reservas = tablereservation_connector.mostrar_todas_reservas()
    return reservas


@app.get("/bar/api/v1/reserva/{reserva_id}")
async def get_reserva(reserva_id: int, q: str | None = None):
    reserva = tablereservation_connector.buscar_reserva(reserva_id)
    return reserva


@app.get("/bar/api/v1/mesas")
async def get_mesas():
    mesas = table_connector.mostrar_mesas_reserva()
    return mesas


@app.get("/bar/api/v1/mesa/{table_id}")
async def get_mesa(table_id: int, q: str | None = None):
    mesa = table_connector.buscar_mesa(table_id)
    return mesa


@app.get("/bar/api/v1/productos")
async def get_productos():
    productos = product_connector.mostrar_todos_productos()
    return productos


@app.get("/bar/api/v1/stock-productos")
async def get_stock_productos():
    productos_stock = product_connector.mostrar_stock()
    return productos_stock


@app.get("/bar/api/v1/producto/{product_id}")
async def get_producto(product_id: int, q: str | None = None):
    producto = product_connector.buscar_un_producto(product_id)
    return producto


@app.get("/bar/api/v1/pedidos")
async def get_pedidos():
    listado_validados = []
    for order in listado_pedidos_actuales:
        pedido = order.to_dict()
        listado_validados.append(pedido)
    return listado_validados


@app.get("/bar/api/v1/pedido/{pedido_id}")
async def get_pedidos(pedido_id: int):
    pedido_seleccionado = []
    for order in listado_pedidos_actuales:
        if order.code == pedido_id:
            pedido = order.to_dict()
            pedido_seleccionado.append(pedido)
    return pedido_seleccionado


@app.get("/bar/api/v1/facturas")
async def get_facturas():
    facturas = invoice_connector.mostrar_todas_facturas()
    return facturas


@app.get("/bar/api/v1/factura/{factura_id}")
async def get_factura(factura_id: int, q: str | None = None):
    factura = invoice_connector.buscar_factura(factura_id)
    return factura


# POST
@app.post("/bar/api/v1/nuevamesa")
async def crear_mesa(nombre: Annotated[str, Form()]):
    mesa = Table(
        code=None,
        name=nombre,
    )
    table_connector.insertar_mesa(mesa)
    print(mesa)
    return mesa


@app.post("/bar/api/v1/nuevoproducto")
async def crear_producto(nombre: Annotated[str, Form()], precio: Annotated[float, Form()], iva: Annotated[int, Form()], stock: Annotated[int, Form()]):
    producto = Product(
        code=None,
        name=nombre,
        price=precio,
        iva=iva,
        stock=stock
    )
    product_connector.insertar_producto(producto)
    print(producto)
    return producto


@app.post("/bar/api/v1/nuevareserva")
async def crear_reserva(mesa_cod: Annotated[int, Form()], fecha: Annotated[str, Form()], num_comensales: Annotated[int, Form()], nota: Annotated[str, Form()]):
    reserva = TableReservation(
        code=None,
        table_code=mesa_cod,
        date=fecha,
        num_people=num_comensales,
        note=nota
    )
    tablereservation_connector.insertar_reserva(reserva)
    print(reserva)
    return reserva


@app.post("/bar/api/v1/nuevopedido")
async def crear_pedido(mesa_cod: Annotated[int, Form()]):
    pedido = iniciar_pedido(mesa_cod)
    print(pedido)
    listado_pedidos_actuales.append(pedido)
    print("Pedidos actuales: ", listado_pedidos_actuales)
    return pedido.to_dict()


@app.post("/bar/api/v1/nuevafactura")
async def crear_factura(cod_pedido: Annotated[int, Form()]):
    for pedido in listado_pedidos_actuales:
        if pedido.code == cod_pedido:
            factura = generar_factura(pedido)
            print(factura)
            # Borrar pedido de la var lista global de pedidos
            listado_pedidos_actuales.remove(pedido)
            return factura
    return


# PUT
@app.put("/bar/api/v1/actualizarproducto/{cod_producto}", response_model=Product | str)
async def modificar_producto(cod_producto: int, product: Product = Body(...)):
    producto = product_connector.buscar_un_producto(cod_producto)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    mensaje = product_connector.modificar_producto(product)
    return mensaje


# crear func updateMesa en db, llamarla y almacenar en mensaje lo que devuelve
@app.put("/bar/api/v1/actualizarmesa/{cod_mesa}", response_model=Table | str)
async def modificar_mesa(cod_mesa: int, table: Table = Body(...)):
    mesa = table_connector.buscar_mesa(cod_mesa)
    if mesa is None:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    mensaje = table_connector.modificar_mesa(table)
    return mensaje


@app.put("/bar/api/v1/actualizarreserva/{cod_reserva}", response_model=TableReservation | str)
async def modificar_reserva(cod_reserva: int, reserva_modificada: TableReservation = Body(...)):
    reserva = tablereservation_connector.buscar_reserva(cod_reserva)
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    mensaje = tablereservation_connector.modificar_reserva(reserva_modificada)
    return mensaje


@app.put("/bar/api/v1/add_productos_pedido/{cod_pedido}")
async def agregar_productos_al_pedido(cod_pedido: int, cod_producto: Annotated[int, Form()], cantidad: Annotated[int, Form()]):
    print("cod_pedido: ", cod_pedido)
    print("cod_producto: ", cod_producto)
    print("cantidad: ", cantidad)

    for order in listado_pedidos_actuales:
        if order.code == cod_pedido:
            order_obj = agregar_al_pedido(order, {cod_producto: cantidad})
            return order_obj.to_OrderDTO()


@app.put("/bar/api/v1/delete_productos_pedido/{cod_pedido}")
async def borrar_productos_del_pedido(cod_pedido: int, cod_producto: Annotated[int, Form()], cantidad: Annotated[int, Form()]):
    for order in listado_pedidos_actuales:
        if order.code == cod_pedido:
            order_obj = eliminar_del_pedido(order, {cod_producto: cantidad})
            return order_obj.to_OrderDTO()


#DELETE
@app.delete("/bar/api/v1/delete_producto")
async def borrar_producto(cod_producto: int):
    producto = product_connector.buscar_un_producto(cod_producto)
    mensaje = product_connector.eliminar_producto(producto)
    return mensaje


@app.delete("/bar/api/v1/delete_mesa")
async def borrar_mesa(cod_mesa: int):
    mesa = table_connector.buscar_mesa(cod_mesa)
    mensaje = table_connector.eliminar_mesa(mesa)
    return mensaje


@app.delete("/bar/api/v1/delete_reserva")
async def borrar_reserva(cod_reserva: int):
    reserva = tablereservation_connector.buscar_reserva(cod_reserva)
    mensaje = tablereservation_connector.eliminar_reserva(reserva)
    return mensaje


@app.delete("/bar/api/v1/delete_pedido")
async def borrar_pedido(cod_pedido: int):
    mensaje = "No se ha encontrado el pedido"
    for order in listado_pedidos_actuales:
        if order.code == cod_pedido:
            listado_pedidos_actuales.remove(order)
            mensaje = "Pedido eliminado con éxito"
    return mensaje


@app.delete("/bar/api/v1/delete_factura")
async def borrar_factura(cod_factura: int):
    factura = invoice_connector.buscar_factura(cod_factura)
    mensaje = invoice_connector.eliminar_factura(factura)
    return mensaje



if __name__ == '__main__':
    print('Hello, I am PyCharm')
    #print(bar_services.mostrar_reservas())


