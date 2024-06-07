const api = "http://127.0.0.1:5000";

window.onload = () => {
    const searchInput = document.getElementById('search_input');
    const searchButton = document.getElementById('button-addon2');
    const productForm = document.getElementById('product_form');

    searchButton.addEventListener('click', searchButtonOnClick);
    productForm.addEventListener('submit', productFormOnSubmit);
}

searchButtonOnClick = () => {
    const searchInput = document.getElementById('search_input');
    const searchQuery = searchInput.value;

    fetch(`${api}/products/search?q=${searchQuery}`)
        .then(response => response.json())
        .then(products => {
            const resultsTableBody = document.getElementById('results-body');
            resultsTableBody.innerHTML = ''; // Clear the table body

            products.forEach((product) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.productionYear}</td>
                    <td>${product.price}</td>
                    <td>${product.color}</td>
                    <td>${product.size}</td>
                    <td><button class="btn btn-primary">Edit</button> <button class="btn btn-danger">Delete</button></td>
                `;
                resultsTableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error searching for products:', error));
}

productFormOnSubmit = (event) => {
    event.preventDefault();

    const nameInput = document.getElementById('new_name');
    const productionYearInput = document.getElementById('new_production_year');
    const priceInput = document.getElementById('new_price');
    const colorInput = document.getElementById('new_color');
    const sizeInput = document.getElementById('new_size');

    const productData = {
        name: nameInput.value,
        productionYear: productionYearInput.value,
        price: priceInput.value,
        color: colorInput.value,
        size: sizeInput.value,
    };

    fetch(`${api}/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(productData),
    })
        .then(response => response.json())
        .then((product) => {
            console.log('Product added successfully!', product);
            // Reset the form fields
            nameInput.value = '';
            productionYearInput.value = '';
            priceInput.value = '';
            colorInput.value = '';
            sizeInput.value = '';
        })
        .catch(error => console.error('Error adding product:', error));
}
