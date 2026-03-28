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

// edit & delete products

async function editProduct(id, name, category, price, description) {
    const newName  = prompt('New name:',        name)
    const newCat   = prompt('New category:',    category)
    const newPrice = prompt('New price:',       price)
    const newDesc  = prompt('New description:', description)

    await fetch(`${API}/products/${id}`, {
        method:  'PUT',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({
            name:        newName,
            category:    newCat,
            price:       newPrice,
            description: newDesc
        })
    })

    loadProducts()
}

async function deleteProduct(id) {
    if (!confirm('Delete this product?')) return

    await fetch(`${API}/products/${id}`, {
        method: 'DELETE'
    })

    loadProducts()
}

//  SHADES

// add new shade

async function addShade() {
    const product_id = document.getElementById('s-product-id').value
    const shade_name = document.getElementById('s-name').value
    const hex_code   = document.getElementById('s-hex').value

    await fetch(`${API}/shades`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ product_id, shade_name, hex_code })
    })

    alert('Shade added!')
}

// load shades for a product

async function loadShades() {
    const id   = document.getElementById('s-search-id').value
    const res  = await fetch(`${API}/shades/${id}`)
    const data = await res.json()

    const div = document.getElementById('shade-list')

    if (data.length === 0) {
        div.innerHTML = '<p>No shades found.</p>'
        return
    }

    div.innerHTML = data.map(s => `
        <div style="display:inline-block; margin:6px; text-align:center">
            <div style="width:50px; height:50px; background:${s.hex_code};
                        border:1px solid #ccc; border-radius:50%"></div>
            <small>${s.shade_name}</small><br>
            <small>${s.hex_code}</small><br>
            <button onclick="editShade(${s.id}, '${s.shade_name}', '${s.hex_code}')">Edit</button>
             <button onclick="deleteShade(${s.id})">Delete</button>
        </div>
    `).join('')
}

async function deleteShade(id) {
    if (!confirm('Delete this shade?')) return

    await fetch(`${API}/shades/${id}`, {
        method: 'DELETE'
    })

    // reload shades for the same product after deletion
    loadShades()
}

// edit shade details
async function editShade(id, shade_name, hex_code) {
    const newName = prompt('New shade name:', shade_name)
    const newHex  = prompt('New hex code:', hex_code)

    if (!newName || !newHex) return
   // hex code should start with # and be 7 characters long
    await fetch(`${API}/shades/${id}`, {
        method:  'PUT',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({
            shade_name: newName,
            hex_code:   newHex
        })
    })

    loadShades()
}

//  BATCH / AUTHENTICITY

// add new batch code for a product

async function addBatch() {
    const product_id = document.getElementById('b-product-id').value
    const batch_code = document.getElementById('b-code').value
    const is_genuine = document.getElementById('b-genuine').value

// is_genuine should be 'true' or 'false' as string

    await fetch(`${API}/batch`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ product_id, batch_code, is_genuine })
    })

    alert('Batch code added!')
}

// verify batch code and show result with QR code
async function verifyBatch() {
    const code = document.getElementById('b-verify').value
    const res  = await fetch(`${API}/batch/verify/${code}`)
    const data = await res.json()

    document.getElementById('verify-result').innerHTML = `
        <h3>Result: ${data.status}</h3>
    `

    // QR code sirf GENUINE products ke liye
    if (data.data && data.data.is_genuine == 1) {
        const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${code}`
        document.getElementById('qr-code').innerHTML = `
            <p>Batch Code QR:</p>
            <img src="${qrUrl}" alt="QR Code">
        `
    } else {
        document.getElementById('qr-code').innerHTML = ''
    }
}

// load all batch codes for a product

let batchTableVisible = false

async function loadBatches() {
    const tbody = document.getElementById('batch-list')
    const table = document.getElementById('batch-table')
    const btn   = document.getElementById('batch-toggle-btn')

    // If the table is already visible, then hide it.
    if (batchTableVisible) {
        table.style.display  = 'none'
        btn.textContent      = 'Load All Batch Codes ▼'
        batchTableVisible    = false
        return
    }

    // If it is hidden, load the data and display it
    const res  = await fetch(`${API}/batch`)
    const data = await res.json()

    tbody.innerHTML = ''

    data.forEach(b => {
        tbody.innerHTML += `
            <tr>
                <td>${b.id}</td>
                <td>${b.product_id}</td>
                <td>${b.batch_code}</td>
                <td>${b.is_genuine == 1 ? 'GENUINE ✅' : 'FAKE ❌'}</td>
                <td>
                    <button onclick="editBatch(${b.id}, '${b.batch_code}', ${b.is_genuine})">Edit</button>
                    <button onclick="deleteBatch(${b.id})">Delete</button>
                </td>
            </tr>
        `
    })

    table.style.display  = 'table'
    btn.textContent      = 'Hide Batch Codes ▲'
    batchTableVisible    = true
}

// edit batch code and genuineness
async function editBatch(id, batch_code, is_genuine) {
    const newCode    = prompt('New batch code:', batch_code)
    const newGenuine = prompt('Genuine? (1 = yes, 0 = no):', is_genuine)

    if (!newCode || newGenuine === null) return

    await fetch(`${API}/batch/${id}`, {
        method:  'PUT',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({
            batch_code:  newCode,
            is_genuine:  parseInt(newGenuine)
        })
    })

    loadBatches()
}

// delete batch code
async function deleteBatch(id) {
    if (!confirm('Delete this batch code?')) return

    await fetch(`${API}/batch/${id}`, {
        method: 'DELETE'
    })

    loadBatches()
}

//  REVIEWS

async function addReview() {
    const product_id = document.getElementById('r-product-id').value
    const reviewer   = document.getElementById('r-reviewer').value
    const rating     = document.getElementById('r-rating').value
    const comment    = document.getElementById('r-comment').value

    await fetch(`${API}/reviews`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ product_id, reviewer, rating, comment })
    })

    alert('Review added!')
    loadReviews()
}

// load reviews for a product
let reviewTableVisible = false

async function loadReviews() {
    const table = document.getElementById('review-table')
    const btn   = document.getElementById('review-toggle-btn')
    const tbody = document.getElementById('review-list')
    
    // If the table is already visible, then hide it.
   if (reviewTableVisible) {
        table.style.display = 'none'
        btn.textContent     = 'Load Reviews ▼'
        reviewTableVisible  = false
        return
    }

    // load reviews and show table
    const res  = await fetch(`${API}/reviews`)
    const data = await res.json()

    tbody.innerHTML = ''

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No reviews found.</td></tr>'
    } else {
        data.forEach(r => {
            tbody.innerHTML += `
                <tr>
                    <td>${r.id}</td>
                    <td>${r.product_name}</td>
                    <td>${r.reviewer}</td>
                    <td>${'⭐'.repeat(r.rating)}</td>
                    <td>${r.comment}</td>
                    <td>
                        <button onclick="deleteReview(${r.id})">Delete</button>
                    </td>
                </tr>
            `
        })
    }

    table.style.display = 'table'
    btn.textContent     = 'Hide Reviews ▲'
    reviewTableVisible  = true
}

// delete review
async function deleteReview(id) {
    if (!confirm('Delete this review?')) return

    await fetch(`${API}/reviews/${id}`, {
        method: 'DELETE'
    })

    loadReviews()
}

//  WISHLIST

let wishlistTableVisible = false

// add product to wishlist for a user
async function addWishlist() {
    const product_id = document.getElementById('w-product-id').value
    const user_name  = document.getElementById('w-user').value

    if (!product_id || !user_name) {
        alert('Please enter Product ID and Your Name!')
        return
    }

// product_id should be a number
    await fetch(`${API}/wishlist`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ product_id, user_name })
    })

    alert('Added to wishlist!')

    // reload wishlist if it is currently visible
    if (wishlistTableVisible) {
        wishlistTableVisible = false
        loadWishlist()
    }
}

// load all wishlist items with product names
async function loadWishlist() {
    const table = document.getElementById('wishlist-table')
    const btn   = document.getElementById('wishlist-toggle-btn')
    const tbody = document.getElementById('wishlist-list')

    // If the table is already visible, then hide it.
    if (wishlistTableVisible) {
        table.style.display  = 'none'
        btn.textContent      = 'Load Wishlist ▼'
        wishlistTableVisible = false
        return
    }

    // load wishlist items and show table
    const res  = await fetch(`${API}/wishlist`)
    const data = await res.json()

    tbody.innerHTML = ''

    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4">No wishlist items found.</td></tr>'
    } else {
        data.forEach(w => {
            tbody.innerHTML += `
                <tr>
                    <td>${w.id}</td>
                    <td>${w.product_name}</td>
                    <td>${w.user_name}</td>
                    <td>
                        <button onclick="removeWishlist(${w.id})">Remove</button>
                    </td>
                </tr>
            `
        })
    }
    // show the table and update button text
    table.style.display  = 'table'
    btn.textContent      = 'Hide Wishlist ▲'
    wishlistTableVisible = true
}

// remove item from wishlist
async function removeWishlist(id) {
    if (!confirm('Remove from wishlist?')) return

    await fetch(`${API}/wishlist/${id}`, {
        method: 'DELETE'
    })

    // Reload karo
    wishlistTableVisible = false
    loadWishlist()
}

// initial load of products

loadProducts()