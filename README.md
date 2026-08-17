# 📚 Library Management System

A full-stack REST API for managing a library — cataloging items, registering members, and handling borrowing, returns, and late fees — with JWT authentication and role-based access control. Built with a clean, layered architecture to demonstrate object-oriented design, the repository pattern, secure authentication, and modern async Python.

🔗 **Live App:** [https://rak5h17a.github.io/library-frontend/](https://rak5h17a.github.io/library-frontend/)
🔗 **Live API Docs:** [https://lib-mgt-sys.onrender.com/docs](https://lib-mgt-sys.onrender.com/docs)

> ⏳ The API is hosted on a free tier that sleeps after inactivity — the **first request may take up to ~50 seconds** to wake the server. Subsequent requests are fast.

---

## ✨ Features

- **Item management** — add and manage books, magazines, and DVDs, each with type-specific loan periods and late-fee rates.
- **Member management** — register students and faculty, each with different borrowing limits and loan-period bonuses.
- **Borrowing & returns** — borrow items with automatic due-date calculation, availability checks, and borrowing-limit enforcement.
- **Late-fee calculation** — fees computed per item type based on days overdue.
- **Authentication & authorization** — JWT-based login with bcrypt password hashing and **role-based access control** (admin vs. member): admins manage the catalog and members; members borrow and return.
- **Interactive API docs** — auto-generated Swagger UI at `/docs`.
- **Web frontend** — a lightweight single-page interface with role-aware UI (admin-only controls appear only for admins).

---

## 🏗️ Architecture

A layered architecture that separates concerns and keeps the codebase testable and maintainable:

```
API Routes  →  Services  →  Repositories  →  MongoDB
                  ↓
            Domain Objects (pure OOP)
```

- **Domain layer** — pure Python objects (`Book`, `Magazine`, `DVD`, `Member`, `Loan`, `User`) implementing the four OOP pillars (encapsulation, abstraction, inheritance, polymorphism) plus composition. No framework code.
- **Repository layer** — abstracts all database access behind a contract (Repository pattern / Dependency Inversion), so the storage backend could be swapped without touching business logic.
- **Service layer** — orchestrates domain objects and repositories to carry out business operations.
- **API layer** — thin FastAPI routes exposing the services over HTTP, with request/response validation via Pydantic schemas and auth guards via dependency injection.

### Three-tier deployment

```
Frontend (HTML/JS)  →  GitHub Pages
Backend (FastAPI)   →  Render (Dockerized)
Database (MongoDB)  →  MongoDB Atlas
```

---

## 🔐 Security

- Passwords are **never stored in plain text** — they are hashed with **bcrypt** (with per-password salting).
- Authentication uses **signed JWTs**; tokens are tamper-proof and expire after a set period.
- **Authorization is enforced on the backend** via dependency-injected guards (`get_current_user`, `require_admin`) — the frontend hides admin controls for UX, but the server is the source of truth.

---

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Framework:** FastAPI
- **Database:** MongoDB (Motor async driver) on MongoDB Atlas
- **Auth:** JWT (python-jose), bcrypt (passlib)
- **Validation:** Pydantic v2
- **Testing:** pytest (20 automated tests — domain logic and API endpoints)
- **Containerization:** Docker
- **Deployment:** Render (backend, auto-deploy from GitHub), GitHub Pages (frontend)
- **Dependency management:** Poetry
- **Frontend:** HTML, CSS, vanilla JavaScript (`fetch`)

---

## 🚀 Running Locally

**Prerequisites:** Python 3.11, Poetry, and a MongoDB connection string (e.g. from MongoDB Atlas).

```bash
# 1. Clone and enter the project
git clone https://github.com/Rak5h17a/Lib_mgt_sys.git
cd Lib_mgt_sys/library-api

# 2. Install dependencies
poetry install

# 3. Create a .env file (see .env.example) with:
#    MONGODB_URL=your_mongodb_connection_string
#    DATABASE_NAME=library_db
#    SECRET_KEY=your_random_secret   (generate: python -c "import secrets; print(secrets.token_hex(32))")

# 4. Run the server
uvicorn app.main:app --reload
```

Then open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the API.

## 🧪 Running Tests

```bash
pytest
```

## 🐳 Running with Docker

```bash
docker build -t library-api .
docker run -p 8000:8000 --env-file .env library-api
```

---

## 📌 Key Endpoints

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `POST` | `/auth/register` | Public | Register a user (admin or member) |
| `POST` | `/auth/login` | Public | Log in, receive a JWT |
| `POST` | `/items/books` | Admin | Add a book |
| `GET`  | `/items/` | Authenticated | List catalog items |
| `POST` | `/members/students` | Admin | Register a student |
| `POST` | `/loans/borrow` | Authenticated | Borrow an item |
| `POST` | `/loans/{loan_id}/return` | Authenticated | Return an item |

---

## 📈 Possible Future Enhancements

- Token refresh & expiry handling
- Linking user accounts to member records (borrow on behalf of yourself only)
- Database transactions for multi-step operations (borrow/return)
- A richer frontend (e.g. React) with full CRUD flows

---

## 👤 Author

**Rakshita** — [GitHub](https://github.com/Rak5h17a)
