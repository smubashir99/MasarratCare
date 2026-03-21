const API = 'http://127.0.0.1:5000'

//  PRODUCTS

async function loadProducts() {
    const res  = await fetch(`${API}/products`)
    const data = await res.json()

    const tbody = document.getElementById('product-list')
    tbody.innerHTML = ''

    data.forEach(p => {
        tbody.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.category}</td>
                <td>Rs. ${p.price}</td>
                <td>${p.description}</td>
                <td>
                    <button onclick="editProduct(${p.id}, '${p.name}',
                        '${p.category}', ${p.price}, '${p.description}')">
                        Edit
                    </button>
                    <button onclick="deleteProduct(${p.id})">
                        Delete
                    </button>
                </td>
            </tr>
        `
    })
}

// add new product

async function addProduct() {
    const name        = document.getElementById('p-name').value
    const category    = document.getElementById('p-category').value
    const price       = document.getElementById('p-price').value
    const description = document.getElementById('p-description').value

    await fetch(`${API}/products`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ name, category, price, description })
    })

    document.getElementById('p-name').value        = ''
    document.getElementById('p-category').value    = ''
    document.getElementById('p-price').value       = ''
    document.getElementById('p-description').value = ''

    loadProducts()
}

// load products on page open
loadProducts()