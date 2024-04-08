// URL del endpoint
const url = 'http://127.0.0.1:8000/bar/api/v1/productos';

// Función para obtener los productos
async function getProducts() {
  const response = await fetch(url);
  const products = await response.json();
  return products;
}

// Función para agregar los productos a la lista
async function addProductsToList() {
  const products = await getProducts();
  const list = document.getElementById('productList');

  products.forEach(product => {
    const listItem = document.createElement('li');
    const productInfo = document.createElement('span');
    productInfo.textContent = `${product.name} - ${product.price}€`; // Concatena nombre de la mesa con su estado
    listItem.appendChild(productInfo);


    list.appendChild(listItem);
  });
}

// Llama a la función cuando se carga la página
window.onload = addProductsToList;