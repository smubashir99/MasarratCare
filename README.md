# MasarratCare

## Product Authenticity & Shade Finder System

**Student Name:** Syed Mubashir Ahmed Hashmi

**Student ID:** 20089221

**Programme:** MSc Information Systems with Computing

**Module:** Programming for information Systems and Computing

**Lecturer:** Paul Laird

**Assignment:** CA2  

**Google Doc Link:** https://docs.google.com/document/d/1vh2IoGhwu9jCHFr-8hoqMELOsc-Cp0xucCnmD6Qz758/edit?usp=sharing

**Date:** 12 April 2026

---

## Table of Contents

| Section | Title                                |
|---------| -------------------------------------|
| 1       | Introduction                         |
| 2       | Organisation & Problem Statement     |
| 3       | System Requirements & Business Rules |
| 4       | Data Requirements & Storage          |
| 5       | System Architecture                  |
| 6       | Implementation                       |
| 7       | Features                             |
| 8       | Testing                              |
| 9       | Tools & Technologies                 |
| 10      | Use of External Resources / AI       |
| 11      | Challenges & Improvements            |
| 12      | Deployment                           |
| 13      | Conclusion                           |
| 14      | References & Attributions            |
| 15      | How to Run the Project               |

---

## 1. Introduction

This project is a web application built to solve the problem of product authenticity and shade selection for Masarrat Misbah Makeup - a real Pakistani cosmetics company identifiable on Google Maps. The company sells products through physical retail shops but has no digital system. Customers cannot verify if their product is genuine or fake, and they struggle to find the right shade for their skin tone.The app allows customers to verify product batch codes, find shades, save products to a wishlist, and leave reviews. Admin users can manage products, shades, and batch codes through a full CRUD interface. The system is built using Python Flask as the backend API, SQLite for data storage, and vanilla JavaScript as the frontend. The app follows a client-server model with REST APIs and no page reloads.

**Live Demo:** https://masarratcare-v5nk.onrender.com/

---

## 2. Organisation & Problem Statement

### Organisation

Masarrat Misbah Makeup is a real Pakistani cosmetics company founded by makeup artist Masarrat Misbah. The company sells premium halal-certified makeup products across Pakistan through physical retail stores.

Google Maps: https://www.google.com/maps/search/?api=1&query=Masarrat+Misbah+Makeup+Lahore

### Current Problem / Inefficiency

The company sells widely across Pakistan but has no digital system:

- Customers buying from physical shops cannot verify if a product is genuine or fake
- Counterfeit products are common in the Pakistani cosmetics market
- Customers have no way to find the correct shade for their skin tone before purchasing
- No platform exists for customers to read or leave product reviews
- No wishlist or save feature for products customers want to buy later

### Why an Information System Is Needed

There is a need for an information system to:

- Allow customers to verify product authenticity using batch codes
- Provide a shade finder with colour visualisation
- Enable customers to read and write product reviews
- Allow customers to save products to a personal wishlist
- Give admin users full control over products, shades, and batch codes

---

## 3. System Requirements & Business Rules

### Functional Requirements

#### User Authentication

- Users can register and log in with username and password
- Login state is saved in localStorage - persists after page refresh
- Two roles: admin and user
- Main content is hidden until login is successful

#### CRUD - Products

- **Create:** Admin can add a new product with name, category, price and description
- **Read:** All users can view all products with prices in PKR and EUR
- **Update:** Admin can edit product name, category, price and description
- **Delete:** Admin can delete a product

#### CRUD - Shades

- **Create:** Admin can add a shade with name and hex colour code
- **Read:** Users can view shades as colour circles for any product
- **Update:** Admin can edit shade name and hex code
- **Delete:** Admin can delete a shade

#### CRUD - Batch Codes

- **Create:** Admin can add batch codes and mark as genuine or fake
- **Read:** All users can view all batch codes in a toggleable table
- **Update:** Admin can edit a batch code
- **Delete:** Admin can delete a batch code

#### Authenticity Checker

- User enters a batch code and clicks verify
- System checks the database and returns GENUINE or FAKE status
- A QR code is generated for genuine products only
- NOT FOUND is returned if batch code does not exist

#### Reviews

- Users can submit a review with name, rating (1-5), and comment
- All reviews are displayed with product name (via SQL JOIN)
- Reviews table toggles open and close
- Users can delete a review

#### Wishlist

- Users can save a product to their wishlist
- Wishlist shows product name (via SQL JOIN)
- Wishlist table toggles open and close
- Users can remove items from wishlist

### Business Rules

**BR01 - Login Required**
All features are hidden until the user logs in successfully.

**BR02 - QR Code Only for Genuine Products**
QR code is generated and displayed only when a batch code is verified as GENUINE. Fake products do not receive a QR code.

**BR03 - Shade Finder by Product**
Shades are linked to a specific product via foreign key. Users must enter a product ID to view its shades.

**BR04 - Auto Seed on First Start**
If the products table is empty on server startup, sample data is automatically inserted - no manual seed command needed.

**BR05 - Currency Conversion**
All product prices are shown in both PKR (Pakistani Rupees) and EUR (Euros) using the Exchange Rate API.

**BR06 - SQL JOIN for Reviews and Wishlist**
Reviews and wishlist items display product names using a SQL LEFT JOIN query - not by storing the name directly.

---

## 4. Data Requirements & Storage

### Entities & Fields

#### Users

| Field    | Type    | Notes                                      |
| -----    | ----    | -----                                      |
| id       | INTEGER | Primary key, auto-increment                |
| username | TEXT    | Unique, required                           |
| password | TEXT    | Plain text (bcrypt improvement identified) |
| role     | TEXT    | admin or user, default user                |

#### Products

| Field       | Type    | Notes                       |
| -----       | ----    | -----                       |
| id          | INTEGER | Primary key, auto-increment |
| name        | TEXT    | Required                    | 
| category    | TEXT    | lips, face, eyes etc.       |
| price       | REAL    | In Pakistani Rupees         |
| description | TEXT    | Product description         |

#### Shades

| Field      | Type    | Notes                       |
| -----      | ----    | -----                       |
| id         | INTEGER | Primary key, auto-increment |
| product_id | INTEGER | Foreign key → products      |
| shade_name | TEXT    | Required                    |
| hex_code   | TEXT    | e.g. #FF69B4              |

#### Batch Codes

| Field      | Type    | Notes                       |
| -----      | ----    | -----                       |
| id         | INTEGER | Primary key, auto-increment |
| product_id | INTEGER | Foreign key → products      |
| batch_code | TEXT    | Unique                      |
| is_genuine | INTEGER | 1 = genuine, 0 = fake       |

#### Reviews

| Field      | Type    | Notes                       |
| -----      | ----    | -----                       |
| id         | INTEGER | Primary key, auto-increment |
| product_id | INTEGER | Foreign key → products      |
| reviewer   | TEXT    | Reviewer name               |
| rating     | INTEGER | 1 to 5                      |
| comment    | TEXT    | Review text                 |

#### Wishlist

| Field      | Type    | Notes                       |
| -----      | ----    | -----                       |
| id         | INTEGER | Primary key, auto-increment |
| product_id | INTEGER | Foreign key → products      |
| user_name  | TEXT    | User who saved it           |

### Relationships

- A **Product** has many **Shades** (one-to-many)
- A **Product** has many **Batch Codes** (one-to-many)
- A **Product** has many **Reviews** (one-to-many)
- A **Product** has many **Wishlist** items (one-to-many)

### Storage Choice

SQLite was chosen as the database. It is a lightweight file-based database built into Python - no separate server installation is required. All data is stored in a single file (medora.db). It supports full SQL including CREATE, INSERT, UPDATE, DELETE and JOIN queries. The assignment explicitly allows SQLite as a valid backend option.

---

## 5. System Architecture

### Overview

- Two-tier architecture: Frontend → API → Database
- Frontend never communicates directly with the database
- All data access goes through the REST API
- No page refresh - JavaScript handles all DOM updates client-side

### Frontend - Vanilla JavaScript (port 5500 local)

- Plain HTML, CSS, and JavaScript - no framework required
- All API calls made via JavaScript fetch() function
- DOM updates happen directly after each API response
- Login state stored in localStorage - persists after page refresh
- Main content hidden via style.display until login is confirmed

### API Layer - Flask REST API (port 5000 local)

- Built with Python Flask
- Each feature has dedicated routes in app.py
- models.py contains all CRUD functions
- db.py manages SQLite connection with row_factory for dict output
- Flask-CORS allows cross-origin requests from the frontend
- All routes return JSON responses

### Database - SQLite

- Single file database: medora.db
- 6 tables with foreign key relationships
- init_db() creates all tables on startup if they do not exist
- auto_seed() inserts sample data if products table is empty

### Request Flow

1. User performs an action in the browser (e.g. clicks Add Product)
2. app.js makes a fetch() call with JSON body and correct HTTP method
3. Flask receives the request and routes it to the correct function
4. The function calls the appropriate model function in models.py
5. models.py runs a SQL query on the SQLite database via db.py
6. Result is returned as JSON to the frontend
7. app.js updates the DOM directly - no page reload

### Deployed Architecture

On Render, Flask serves both the API and the frontend:

Browser → https://masarratcare-v5nk.onrender.com
→ Flask (gunicorn)
→ Serves index.html (static file)
→ API calls go to same server (/products, /shades etc.)
→ SQLite database (medora.db)
→ auto_seed() runs on startup

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

---

## 6. Implementation

### Backend

#### Project Structure

- Flask backend with SQLite database
- Database layer handles connection setup and initialization of 6 tables
- Models layer contains all CRUD operations for the database
- Main entry point (app.py) defines API routes, serves frontend static files, and runs auto_seed() on startup
- Separate seed script available for manual database seeding during local development

#### db.py

- `get_db()` - opens SQLite connection with row_factory = sqlite3.Row
- `init_db()` - creates all 6 tables using CREATE TABLE IF NOT EXISTS
- row_factory converts rows to dictionaries for easy JSON conversion

#### models.py

- One set of CRUD functions per table
- All functions use get_db() for consistent connection management
- dict(r) used to convert Row objects to plain Python dictionaries
- verify_batch() returns None if batch code is not found

#### app.py

- Flask app configured with static_folder pointing to frontend/
- CORS(app) applied globally
- auto_seed() checks if products table is empty on startup
- If empty, inserts 3 products, 9 shades, 6 batch codes, 2 users
- @app.route('/') serves index.html directly
- All other routes serve the REST API

### Frontend

#### Project Structure

- Vanilla JavaScript frontend architecture
- Single-page layout handled in index.html with sections for login, products, shades, authenticity, reviews, and wishlist
- app.js manages API calls using fetch() and updates the DOM dynamically
- Global styling provided via style.css using the Pink Poppins theme
- Environment configuration handled through config.json for API base URL

#### Authentication Flow

- Login section shown on page load
- loginUser() sends POST /login with username and password
- On success, user data saved to localStorage
- Main content div shown, login section hidden
- On page refresh, localStorage checked - if user exists, skip login
- logoutUser() clears localStorage and shows login again

#### fetch() Pattern

All operations follow the same pattern:

```javascript
async function addProduct() {
    const name = document.getElementById('p-name').value
    await fetch(`${API}/products`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ name, category, price, description })
    })
    loadProducts()  // refresh list - no page reload
}
```

---

## 7. Features

### Core Features

#### CRUD - Products

- Add product with name, category, price, description
- View all products - prices shown in PKR and EUR via Exchange Rate API
- Edit product using prompt dialogs
- Delete product with confirm dialog
- Table updates dynamically after every operation

#### CRUD - Shades

- Add shade with product ID, shade name, hex colour code
- View shades as colour circles with hex codes
- Edit shade name and hex code
- Delete shade
- Colour circles update immediately

#### CRUD - Batch Codes

- Add batch code with product ID and genuine/fake status
- View all batch codes in a toggleable table
- Edit batch code and genuine status
- Delete batch code

#### Authenticity Checker

- Enter batch code and click verify
- Returns GENUINE ✅, FAKE ❌, or NOT FOUND ❓
- QR code generated via QR Server API for genuine products only
- Toggle table to view all batch codes

#### Reviews

- Add review with product ID, name, rating (1-5), comment
- View all reviews - product name shown via SQL JOIN
- Toggle table open and close
- Delete review

#### Wishlist

- Add product to wishlist with product ID and name
- View all wishlist items - product name via SQL JOIN
- Toggle table open and close
- Remove item from wishlist

### Additional Features

#### Login & Register System

- Register new account with username and password
- Login with username and password
- Enter key supported on login and register forms
- Login state persists after page refresh via localStorage
- Logout clears localStorage

#### Currency Conversion

- Exchange Rate API called on every product load
- Converts PKR price to EUR in real time
- Both currencies shown in products table

#### QR Code Generation

- QR Server API called after successful authenticity check
- QR code image displayed only for GENUINE products
- No QR code for FAKE or NOT FOUND results

#### Toggle Tables

- Batch codes, reviews, and wishlist tables toggle open/close
- Button text changes between Load ▼ and Hide ▲

---

## 8. Testing

### Overview

- Unit tests written using pytest
- Tests run at the model layer - direct database calls
- conftest.py initialises the database before tests run
- One test file per model - one test file for integration

### Unit Tests

#### test_models_product.py

| Test                  | Expected Result                                    |
| ----                  | ---------------                                    |
| test_create_product   | Product is created and found in get_all_products() |
| test_get_all_products | Returns a non-empty list                           |
| test_delete_product   | Deleted product no longer appears in list          |

#### test_models_shade.py

| Test                       | Expected Result                                       |
|---|---|
| test_create_shade          | Shade is created and found in get_shades_by_product() |
| test_get_shades_by_product | Returns a list                                        |
| test_delete_shade          | Deleted shade no longer appears in list               |

#### test_models_batch.py

| Test                       | Expected Result                                     |
| ---                        | ---------------                                     |
| test_create_batch          | Batch code is created and verify_batch() returns it |
| test_verify_genuine_batch  | is_genuine returns 1                                |
| test_verify_fake_batch     | is_genuine returns 0                                |
| test_verify_notfound_batch | Returns None                                        |

#### test_models_review.py

| Test               | Expected Result                     |
| ----               | ---------------                     |
| test_create_review | Review is created and found in list |
| test_get_reviews   | Returns a list                      |
| test_delete_review | Deleted review no longer appears    |

#### test_models_wishlist.py

| Test                 | Expected Result                    |
| ----                 | ---------------                    |
| test_add_wishlist    | Wishlist item is created and found |
| test_get_wishlist    | Returns a list                     |
| test_remove_wishlist | Removed item no longer appears     |

### Integration Test

#### test_ping.py

| Test              | Expected Result                                      |
| ---               | ---------------                                      |
| test_ping         | GET /ping returns status 200 and {"message": "pong"} |
| test_get_products | GET /products returns status 200 and a list          |

This test sends a real HTTP request to the running Flask server, confirming that the frontend can talk to the backend end-to-end.

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Result
18 passed in 0.18s
```

---

## 9. Tools & Technologies

### Runtime & Language

| Tool       | Version | Purpose              |
| ----       | ---     | -------              |
| Python     | 3.14    | Server-side language |
| JavaScript | ES6+    | Frontend language    |

### Backend

| Tool       | Version  | Purpose                           |
| ----       | -------  | -------                           |
| Flask      | 3.1.3    | Backend API framework             |
| Flask-CORS | 6.0.2    | Cross-origin request handling     |
| gunicorn   | Latest   | Production WSGI server for Render |
| SQLite     | Built-in | Lightweight file-based database   |

### Frontend

| Tool       | Version | Purpose                       |
| ---        | ------- | -------                       |
| HTML5      | -       | Page structure and forms      |
| CSS3       | -       | Styling with Poppins font     |
| JavaScript | ES6+    | fetch() calls and DOM updates |

### Testing

| Tool     | Version | Purpose                        |
| ----     | ------- | -------                        |
| pytest   | 9.0.2   | Unit and integration testing   |
| requests | 2.32.5  | HTTP calls in integration test |

### External APIs

| API               | Purpose                                  | Docs                 |
| ---               | ---------------------------------------- | ----                 |
| QR Server API     | Generate QR code for genuine batch codes | goqr.me/api          |
| Exchange Rate API | Convert PKR to EUR for product prices    | exchangerate-api.com |

### Development Tools

| Tool                  | Purpose                               |
| ----                  | -------                               |
| VS Code               | Code editor                           |
| GitHub                | Version control and remote repository |
| Windows Terminal      | Running Flask and pytest              |
| Live Server (VS Code) | Local frontend serving                |
| Render                | Cloud deployment platform             |

---

## 10. Use of External Resources / AI

### Frameworks & Libraries

| Resource             | Source                    | What It Provided                | What Was Built On Top          |
| --------             | ------                    | ----------------                | ------------------           |
| Flask                | flask.palletsprojects.com | Routing, request handling, JSON | All API routes, auto_seed, frontend serving |
| Flask-CORS           | flask-cors.readthedocs.io | Cross-origin middleware         | Applied globally to allow frontend calls |
| pytest               | pytest.org                | Test runner and assertions      | 18 tests across 6 test files |
| QR Server API        | goqr.me/api               | QR image generation URL         | Business logic - only genuine products get QR |
| Exchange Rate API    | exchangerate-api.com      | Live PKR to EUR rate            | Integrated into loadProducts() in app.js |
| Google Fonts Poppins | fonts.google.com          | Poppins font family             | Applied globally in style.css |

### AI Usage

This project was developed with the assistance of Claude (Anthropic) 
and ChatGPT as co-pilot tools.

#### What AI Was Used For

- Recalling Python INSERT query syntax for reviews model
- Route parameter syntax for Flask int:id routes
- Inline CSS styling pattern for shade colour circles
- assert any() pattern for pytest test assertions
- CSS styling guidance for the pink Poppins theme
- Wording improvements for this README file

#### How AI Output Was Used

- All AI-generated code was reviewed before use
- Several parts required manual correction:
  - db.py path used "medora.db" directly - caused 
    OperationalError on Render - fixed with os.path
  - app.js API URL used localhost - broke on Render - 
    fixed to use relative URL ('')
  - conftest.py was needed to fix "no such table" error 
    in pytest - added sys.path and init_db() call
  - verifyBatch() showed QR for fake products - fixed 
    with is_genuine == 1 condition check
- AI was used as a productivity tool - not a replacement 
  for understanding
- All generated code was tested, debugged, and modified

### Attribution Summary

| Resource             | Licence             | Link                      |
| --------             | -------             | ----                      |
| Flask                | BSD-3-Clause        | flask.palletsprojects.com |
| Flask-CORS           | MIT                 | flask-cors.readthedocs.io |
| pytest               | MIT                 | pytest.org                |
| requests             | Apache 2.0          | requests.readthedocs.io   |
| SQLite               | Public Domain       | sqlite.org                |
| QR Server API        | Free non-commercial | goqr.me/api               |
| Exchange Rate API    | Free tier           | exchangerate-api.com      |
| Google Fonts Poppins | Open Font License   | fonts.google.com          |
| Render | Free tier   | render.com          |
| Claude (Anthropic)   | N/A - AI tool       | anthropic.com             |
| ChatGPT (OpenAI)     | N/A - AI tool       | openai.com                |

I have used Chrome and AI tools to help with specific parts of the code. All AI usage is referenced in GitHub commit messages. The overall idea, system design, architecture decisions and majority of the code is my own work.

---

## 11. Challenges & Improvements

### Challenges Faced

#### 1. SQLite Path Issue on Render

- Local development used "medora.db" as the database path
- On Render, the working directory is different from the file location
- Flask could not find the database file - caused OperationalError
- **Fix:** Used os.path.dirname(os.path.abspath(__file__)) to build an absolute path to medora.db relative to db.py

#### 2. API URL Breaking on Render

- Local frontend used const API = 'http://127.0.0.1:5000'
- On Render, frontend and backend run on the same server
- Absolute localhost URL caused CORS and connection errors
- **Fix:** Changed API URL to empty string '' so fetch() uses relative URLs - works both locally and on Render

#### 3. pytest "no such table" Error

- Tests ran from the project root, not from the backend folder
- SQLite could not find the tables because init_db() was not called
- **Fix:** Added conftest.py to tests/ folder - adds backend to sys.path and calls init_db() before any test runs

#### 4. QR Code Showing for Fake Products

- verifyBatch() returned data for both genuine and fake products
- QR code was being generated for all verified codes including FAKE
- **Fix:** Added is_genuine == 1 check before generating QR URL in verifyBatch() in app.js

#### 5. Login Not Persisting After Refresh

- On page refresh, localStorage was not being checked
- User was sent back to login screen after every refresh
- **Fix:** Added savedUser check on page load - if localStorage has a user, skip login and show main content directly

### What Would Be Improved With More Time

#### Security Improvements

- Password hashing using bcrypt - currently stored as plain text
- Proper session tokens instead of localStorage
- JWT authentication for API routes

#### Technical Improvements

- Switch from SQLite to PostgreSQL for persistent cloud database
- SQLite resets on Render redeploy - PostgreSQL would persist data
- Add pagination to products and reviews lists
- Add search functionality for products by name or category
- Add image upload for products

#### Frontend Improvements

- Add form validation with error messages instead of browser alerts
- Add loading indicators while fetch() calls are in progress
- Make UI fully responsive for mobile screens

---

## 12. Deployment

### Overview

The application is deployed on Render - a free cloud hosting platform. Flask serves both the backend API and the frontend static files from the same instance.

**Live URL:** https://masarratcare-v5nk.onrender.com/

### Deployment Configuration

A render.yaml file was added to the root folder:

```yaml
services:
  - type: web
    name: masarratcare
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --chdir backend app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

| Setting       | Value                              |
| -------       | -----                              |
| Platform      | Render                             |
| Runtime       | Python 3.11                        |
| Region        | Frankfurt (EU) - closest to Dublin |
| Build Command | pip install -r requirements.txt    |
| Start Command | gunicorn --chdir backend app:app   |
| Plan          | Free                               |

### Frontend Serving on Render

Flask serves the frontend directly - no separate hosting needed:

```python
app = Flask(
    __name__,
    static_folder='../frontend',
    static_url_path=''
)

@app.route('/')
def index():
    return app.send_static_file('index.html')
```

### Auto Seed on Startup

Since Render free plan resets SQLite on redeploy, auto_seed() was added to app.py. It runs on every server start:

- Checks if products table is empty
- If empty - inserts 3 products, 9 shades, 6 batch codes, 2 users
- If not empty - skips seeding

No manual seed command needed after deployment.

### Important Note on Free Plan

Render free plan sleeps after 15 minutes of inactivity. The first visit may take 30-60 seconds to wake up the server. After that, all requests are fast.

---

## 13. Conclusion

- Built a fully functional Product Authenticity and Shade Finder System for Masarrat Misbah Makeup
- System meets the core assignment requirements:
  - REST API architecture with frontend making fetch() calls - no page refresh
  - Full CRUD operations across products, shades, batch codes, reviews, and wishlist
  - JavaScript frontend with Python Flask backend
  - SQLite database with structured schema and foreign key relationships
- Login and register system with localStorage persistence
- Two external APIs integrated - QR Server and Exchange Rate
- 18 unit and integration tests passing with pytest
- Application deployed live on Render at https://masarratcare-v5nk.onrender.com/
- All external libraries and AI usage clearly attributed in commit messages and this README

---

## 14. References & Attributions

### Frameworks & Libraries

- Flask - BSD-3-Clause - https://flask.palletsprojects.com
- Flask-CORS - MIT - https://flask-cors.readthedocs.io
- pytest - MIT - https://pytest.org
- requests - Apache 2.0 - https://requests.readthedocs.io
- SQLite - Public Domain - https://sqlite.org
- Gunicorn - MIT - https://gunicorn.org
- QR Server API - Free non-commercial - https://goqr.me/api
- Exchange Rate API - Free tier - https://exchangerate-api.com
- Google Fonts Poppins - OFL - https://fonts.google.com

### Commit by Commit References

- Commit 1 - creating project structure with backend, frontend and tests folders

- Commit 2 - adding README, gitignore and project dependencies

- Commit 3 - adding get_db function with sqlite connection and row_factory
  - [SQLite Python Documentation](https://docs.python.org/3/library/sqlite3.html)

- Commit 4 - adding products and shades tables with foreign key relationship

- Commit 5 - adding batch_codes, reviews and wishlist tables
  - [SQLite Foreign Keys](https://www.sqlite.org/foreignkeys.html)

- Commit 6 - adding product CRUD functions in models.py

- Commit 7 - adding shade CRUD functions in models.py

- Commit 8 - adding batch, review and wishlist functions
  - Ref: ChatGPT helped with INSERT query syntax for reviews

- Commit 9 - adding basic flask app with cors and ping route
  - [Flask Documentation](https://flask.palletsprojects.com)
  - [Flask-CORS Documentation](https://flask-cors.readthedocs.io)

- Commit 10 - adding product API routes GET POST PUT DELETE

- Commit 11 - adding shade API routes
  - Ref: ChatGPT helped with route parameter syntax for int:id

- Commit 12 - adding batch authenticity routes

- Commit 13 - adding seed data - 3 MM products, 9 shades, batch codes

- Commit 14 - adding html structure with products section

- Commit 15 - adding shade finder and authenticity sections

- Commit 16 - adding basic styling and config file
  - Ref: ChatGPT helped with CSS styling
  - [Google Fonts Poppins](https://fonts.google.com/specimen/Poppins)

- Commit 17 - adding loadProducts and addProduct fetch() functions

- Commit 18 - adding editProduct and deleteProduct functions

- Commit 19 - adding shade and authenticity functions
  - Ref: ChatGPT helped with inline style for colour circles
  - Ref: qrserver.com API docs for QR URL format
  - [QR Server API](https://goqr.me/api)

- Commit 20 - adding integration test test_ping.py

- Commit 21 - adding product unit tests

- Commit 22 - adding shade unit tests

- Commit 23 - adding batch unit tests

- Commit 24 - adding review unit tests
  - Ref: ChatGPT helped with assert any() pattern

- Commit 25 - adding wishlist unit tests

- Commit 26 - adding conftest.py to fix test DB path issue

- Commit 27 - updating README with complete documentation

- Commit 28 - improving UI styling - clean professional look
  - Ref: Google Fonts Poppins for typography
  - [Google Fonts](https://fonts.google.com)

- Commit 29 - adding login and register functionality

- Commit 30 - adding toggle functionality for batch codes table

- Commit 31 - fixing login persistence using localStorage

- Commit 32 - adding Reviews section frontend and API routes

- Commit 33 - adding Wishlist section frontend and API routes

- Commit 34 - adding currency conversion using Exchange Rate API
  - Ref: exchangerate-api.com docs
  - [Exchange Rate API](https://api.exchangerate-api.com)

- Commit 35 - adding render deployment config - gunicorn, 
  render.yaml, frontend serving, auto seed

- Commit 36 - fixing sqlite db path for Render deployment

- Commit 37 - fixing API URL for Render - changed to 
  relative URL

- Commit 38 - fixing QR code to show only for genuine products

---

## 15. How to Run the Project

### Prerequisites

- Python 3.11 or higher
- pip

### Local Setup

Clone the repository:

```bash
git clone https://github.com/smubashir99/MasarratCare.git
cd MasarratCare
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend:

```bash
cd backend
python app.py
```

Open the frontend in VS Code:

frontend/index.html → Right Click → Open with Live Server

Opens on: http://127.0.0.1:5500

### Default Login Credentials

| Username | Password | Role |
|---|---|---|
| admin | admin123 | Admin |
| user1 | user123 | User |

### Seed Data (Local Only)

```bash
cd backend
python seed.py
```

### Run Tests

```bash
python -m pytest tests/ -v
```

Expected result: 18 passed

### Test Batch Codes

| Batch Code     | Status      |
| ----------     | -----       |
| MM-LG-2024-001 | GENUINE ✅ |
| MM-LG-2024-002 | GENUINE ✅ |
| MM-SF-2024-001 | GENUINE ✅ |
| MM-ES-2024-001 | GENUINE ✅ |
| FAKE-001       | FAKE ❌    |
| FAKE-002       | FAKE ❌    |

### Live Demo

No setup needed - just open the link:

https://masarratcare-v5nk.onrender.com/

Note: First visit may take 30-60 seconds if the server is asleep.
