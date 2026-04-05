# MasarratCare

**Student Name:** Syed Mubashir Ahmed Hashmi  
**Student ID:** 20089221
**Programme:** MSc Information Systems with Computing  
**Lecturer Name:** Paul Laird | Dublin Business School  
**Module Title:** Programming for Information Systems
**Assignment Title:** CA2
**Project Title:** MasarratCare - Product Authenticity and Shade Finder System

## Why I picked this company

I chose Masarrat Misbah Makeup because its a real Pakistani cosmetics brand that I actually know from back home. You can find them on Google Maps:
https://www.google.com/maps/search/?api=1&query=Masarrat+Misbah+Makeup+Lahore

The problem I noticed is that the company sells through physical shops but has no digital system. Customers cant tell if a product is real or fake, and they struggle to find the right shade. I thought this was a good real-world problem to solve for this project.

## What the system does

MasarratCare is a web app I built using Flask, SQLite and vanilla JavaScript. The main features are:

- login and register system
- check if a product batch code is genuine or fake
- QR code generated for genuine products only
- find shades for a product with colour circles
- price shown in both PKR and EUR using currency API
- add products to a wishlist
- leave reviews for products
- full admin control - add, edit, delete products/shades/batches

## Project Structure

MasarratCare/
│
├── backend/
│ ├── db.py — sets up SQLite database and 6 tables
│ ├── models.py — all the CRUD functions
│ ├── app.py — Flask routes (the API)
│ └── seed.py — adds sample data and default users
│
├── frontend/
│ ├── index.html — main page with all sections
│ ├── app.js — fetch() calls to the API
│ ├── style.css — pink theme using Poppins font
│ └── config.json — stores the API base URL
│
├── tests/
│ ├── conftest.py — sets up DB before tests run
│ ├── test_ping.py — integration test
│ ├── test_models_product.py — product unit tests
│ ├── test_models_shade.py — shade unit tests
│ ├── test_models_batch.py — batch unit tests
│ ├── test_models_review.py — review unit tests
│ └── test_models_wishlist.py — wishlist unit tests
│
├── requirements.txt
├── README.md
└── .gitignore

## How to run it

first install the requirements:
```bash
pip install -r requirements.txt
```

then start the backend — keep this terminal open:
```bash
cd backend
python app.py
```

add the sample data and default users:
```bash
python seed.py
```

then open frontend/index.html using Live Server in VS Code.
opens on http://127.0.0.1:5500

default login credentials:
- admin: username = admin | password = admin123
- user:  username = user1 | password = user123

## Architecture

the frontend never refreshes the page - everything goes through fetch() calls to the Flask API. Flask talks to SQLite and sends back JSON. the frontend then updates the DOM directly.

index.html + app.js  →  fetch()  →  Flask API  →  SQLite
          ←  JSON response  ←

I added CORS so the browser doesnt block requests between different ports. login state is saved in localStorage so user stays logged in after page refresh.

## Database

I used SQLite with 6 tables, all linked to products 
using foreign keys:

| table | what it stores |
|---|---|
| users | username, password, role |
| products | name, category, price, description |
| shades | shade name and hex colour code |
| batch_codes | batch number and genuine/fake flag |
| reviews | reviewer name, rating, comment |
| wishlist | product saved by a user |
