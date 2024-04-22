let listado_productos = []


// DEVUELVE TODOS LOS CONTACTOS
async function obtenerDatos() {
    try {
        const response = await fetch('http://127.0.0.1:8000/bar/api/v1/productos'); // Cambia la URL según tu configuración
        const data = await response.json();

        // Accede a los datos específicos que deseas mostrar (por ejemplo, trabajadores)
        const productos = data;

        // da el valor a la variable global
        listado_productos = productos

        // Obtén la tabla
        const tabla = document.getElementById('tabla-productos');


        // Supongamos que 'tabla' es tu elemento de tabla
        let filaNombreColumnas = tabla.insertRow();

        // Para cada nombre de columna
        let nombresColumnas = ['CODIGO', 'NOMBRE', 'PRECIO', 'IVA', 'STOCK'];
        for(let i = 0; i < nombresColumnas.length; i++){
            let th = document.createElement('th');
            let texto = document.createTextNode(nombresColumnas[i]);
            th.appendChild(texto);
            filaNombreColumnas.appendChild(th);
        }




        // Agrega filas a la tabla con los datos de los trabajadores
        productos.forEach(producto => {
            const fila = tabla.insertRow();
            fila.setAttribute("data-id", producto.id)
            fila.setAttribute("class", "fila")

            const celdaId = fila.insertCell(0)
            const celdaNombre = fila.insertCell(1);
            const celdaPrecio = fila.insertCell(2);
            const celdaIva = fila.insertCell(3);
            const celdaStock = fila.insertCell(4);


            celdaId.textContent = producto.code;
            celdaNombre.textContent = producto.name;
            celdaPrecio.textContent = producto.price;
            celdaIva.textContent = producto.iva;
            celdaStock.textContent = producto.stock;

        });
    } catch (error) {
        console.error('Error al obtener los datos:', error);
    }
}




// FUNCION QUE BUSCA UN PRODUCTO POR SU ID
async function buscar() {

    let productEncontrado;

    const idBuscado = document.getElementById('buscar-id').value; // Obtener el valor ingresado
    console.log("Valor...", idBuscado)

    // HAY QUE CAMBIAR LA BUSQUEDA EN EL LISTADO POR LA BUSQUEDA
    // EN LO QUE DEVUELVE LA PETICION GET PRODUCTO{ID}
    /*
    console.log("Listado productos...", listado_productos);
    for (let dic_producto of listado_productos){
        let valor_id = dic_producto["id"];
        console.log("producto", valor_id)
        if (valor_id == idBuscado){
            alert("El producto existe!!");
            productEncontrado = dic_producto;
            break;
        }
    }
    */
    const response = await fetch('http://127.0.0.1:8000/bar/api/v1/producto/'+ idBuscado); // Cambia la URL según tu configuración
    const data = await response.json();

    // Accede a los datos específicos que deseas mostrar (por ejemplo, trabajadores)
    productEncontrado = data;


    console.log(productEncontrado)

    if (productEncontrado) {
        console.log('Producto encontrado:', productEncontrado);
        // Aquí puedes hacer lo que necesites con el registro encontrado (por ejemplo, mostrarlo en la página)
        // Obtén la tabla
        const tabla = document.getElementById('tabla-productos');

        console.log("Tabla : ", tabla);

        // selecciona todas las filas de la tabla
        const filas = document.querySelectorAll("#tabla-productos tr");

        // recorre todas las filas, y pone sus celdas en rojo si es el registro coincidente
        filas.forEach(fila => {
            const celdaId = fila.cells[0];
            console.log("fila.cells[0]...", fila.cells[0])
            if (celdaId.textContent == idBuscado){
                celdaId.style.color = "red";
                fila.cells[1].style.color = "red";
                fila.cells[2].style.color = "red";
                fila.cells[3].style.color = "red";
                fila.cells[4].style.color = "red";
            }
            else{
                celdaId.style.color = "black";
                fila.cells[1].style.color = "black";
                fila.cells[2].style.color = "black";
                fila.cells[3].style.color = "black";
                fila.cells[4].style.color = "black";
            }
        })


    } else {
        console.log('No se encontró ningún registro con ese ID.');
        }
    }



// Llama a la función para obtener y mostrar los datos
obtenerDatos();
console.log("Ha llegado hasta aqui")



function manejarClicFila(evento) {
    // pone todas las celdas en color negro
    function ponerCeldasNegras() {
        const filas = document.querySelectorAll('tr'); // Obtiene todas las filas de la tabla

        filas.forEach(fila => { // Recorre cada fila
        const celdas = fila.querySelectorAll('td'); // Obtiene las celdas de la fila actual

        celdas.forEach(celda => { // Recorre cada celda de la fila actual
          celda.style.color = 'black'; // Cambia el color del texto de la celda a negro
        });
        });
        }

    ponerCeldasNegras();

  const filaSeleccionada = evento.target.closest('tr'); // Obtiene la fila más cercana al elemento donde se hizo clic
  if (filaSeleccionada && filaSeleccionada.classList.contains('fila')) { // Verifica si es una fila válida
    const celdas = filaSeleccionada.querySelectorAll('td');
    const datosFila = [];

    // recorre las celdas de la fila seleccionada recogiendo los datos y pintandola en rojo
    for (const celda of celdas) {
        datosFila.push(celda.textContent);
        celda.style.color = 'red';

    }

    console.log("Datos de la fila:", datosFila);
  }
}

const tabla = document.querySelector('table');
console.log(tabla)

tabla.addEventListener('click', manejarClicFila);

