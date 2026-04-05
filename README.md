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

## API routes

| method | route | what it does |
|---|---|---|
| POST | /register | creates new user account |
| POST | /login | checks credentials, returns user info |
| GET | /ping | checks server is alive |
| GET | /products | returns all products with EUR price |
| POST | /products | adds a new product |
| PUT | /products/\<id\> | edits a product |
| DELETE | /products/\<id\> | deletes a product |
| GET | /shades/\<id\> | gets shades for a product |
| POST | /shades | adds a shade |
| PUT | /shades/\<id\> | edits a shade |
| DELETE | /shades/\<id\> | deletes a shade |
| POST | /batch | adds a batch code |
| GET | /batch/verify/\<code\> | checks genuine or fake |
| GET | /batch | gets all batch codes |
| PUT | /batch/\<id\> | edits a batch code |
| DELETE | /batch/\<id\> | deletes a batch code |
| GET | /reviews | gets all reviews with product name |
| POST | /reviews | adds a review |
| DELETE | /reviews/\<id\> | deletes a review |
| GET | /wishlist | gets wishlist with product names |
| POST | /wishlist | adds to wishlist |
| DELETE | /wishlist/\<id\> | removes from wishlist |

## External APIs used

**1. QR Server API** — https://goqr.me/api  
generates a QR code image when a batch code is verified as genuine. only shows for genuine products not fake ones. no api key needed, its free.

**2. Exchange Rate API** — https://api.exchangerate-api.com  
converts product prices from PKR to EUR. shows both currencies in the products table. relevant since this is being presented in Dublin!

## Testing

to run all tests:
```bash
python -m pytest tests/ -v
```

I wrote 5 unit test files, one for each model. each file tests the basic create, read and delete functions.

the integration test (test_ping.py) actually sends a real HTTP request to the running flask server and checks the response. that one needs the server running first.

all 18 tests passed:
18 passed in 0.18s

unit tests:
- test_models_product.py  — create, read, delete product
- test_models_shade.py    — create, read, delete shade
- test_models_batch.py    — genuine, fake, not found
- test_models_review.py   — create, read, delete review
- test_models_wishlist.py — add, get, remove wishlist

integration test:
- test_ping.py — sends HTTP GET to /ping and /products,
  checks status 200 and correct JSON response

## Test batch codes

after running seed.py these batch codes work:

genuine: MM-LG-2024-001, MM-LG-2024-002,
         MM-SF-2024-001, MM-ES-2024-001

fake: FAKE-001, FAKE-002

## What I would improve

if I had more time I would add:
- password hashing using bcrypt for better security
- proper session tokens instead of localStorage
- image upload for each product
- better shade matching using a photo upload

## References

All references are mentioned in GitHub commit messages and inside code comments throughout the project.

### External Libraries and Tools

| # | Reference | Link | License | Used In |
|---|---|---|---|---|
| 1 | Flask | https://flask.palletsprojects.com | BSD-3-Clause | backend/app.py — main server framework |
| 2 | Flask-CORS | https://flask-cors.readthedocs.io | MIT | backend/app.py — cross origin requests |
| 3 | pytest | https://pytest.org | MIT | tests/ — all test files |
| 4 | requests | https://requests.readthedocs.io | Apache 2.0 | tests/test_ping.py — integration test |
| 5 | SQLite | https://sqlite.org | Public Domain | backend/db.py — database |
| 6 | QR Server API | https://goqr.me/api | Free non-commercial | frontend/app.js — verifyBatch() function |
| 7 | Exchange Rate API | https://exchangerate-api.com | Free tier | frontend/app.js — getEURPrice() function |
| 8 | Google Fonts Poppins | https://fonts.google.com | Open Font License | frontend/style.css — typography |

### AI and Online Help

| # | What | Where Used | Commit Reference |
|---|---|---|---|
| 1 | ChatGPT — helped recall INSERT query syntax | backend/models.py — create_review() | commit: "Ref: ChatGPT helped with INSERT query syntax for reviews" |
| 2 | ChatGPT — route parameter syntax for int:id | backend/app.py — shade routes | commit: "Ref: ChatGPT helped with route parameter syntax" |
| 3 | ChatGPT — inline style for colour circles | frontend/app.js — loadShades() | commit: "Ref: ChatGPT helped with inline style for colour circles" |
| 4 | ChatGPT — assert any() pattern for tests | tests/test_models_review.py | commit: "Ref: ChatGPT helped with assert any() pattern" |
| 5 | ChatGPT — CSS styling guidance | frontend/style.css | commit: "Ref: ChatGPT helped with CSS styling" |
| 6 | QR Server API docs — URL format | frontend/app.js — verifyBatch() | commit: "Ref: qrserver.com API docs for url format" |
| 7 | exchangerate-api.com docs | frontend/app.js — getEURPrice() | commit: "Ref: exchangerate-api.com" |
| 8 | Google Fonts docs | frontend/style.css | commit: "Ref: Google Fonts Poppins for typography" |

I have used Chrome and AI tools to help with specific parts of the code. All AI usage is referenced in GitHub commit messages. The overall idea, system design, architecture decisions and majority of the code is my own work.