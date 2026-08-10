# 📚 Library Management System API

A production-style REST API for managing a library — cataloging items, registering members, and handling borrowing, returns, and late fees. Built with a clean, layered architecture to demonstrate object-oriented design, the repository pattern, and modern async Python.

🔗 **Live API:** [https://lib-mgt-sys.onrender.com/docs](https://lib-mgt-sys.onrender.com/docs)
*(Free tier — the first request after inactivity may take ~50 seconds to wake the server.)*

---

## ✨ Features

- **Item management** — add and manage books, magazines, and DVDs, each with type-specific loan periods and late-fee rates.
- **Member management** — register students and faculty, each with different borrowing limits and loan-period bonuses.
- **Borrowing & returns** — borrow items with automatic due-date calculation, availability checks, and borrowing-limit enforcement.
- **Late-fee calculation** — fees computed per item type based on days overdue.
- **Interactive API docs** — auto-generated Swagger UI at `/docs`.

## 🏗️ Architecture

The project uses a layered architecture that separates concerns and keeps the codebase testable and maintainable:

- **Domain layer** — pure Python objects (`Book`, `Magazine`, `DVD`, `Member`, `Loan`) implementing all four OOP pillars (encapsulation, abstraction, inheritance, polymorphism) plus composition. No framework code.
- **Repository layer** — abstracts all database access behind a contract (Repository pattern / Dependency Inversion), so the storage backend could be swapped without touching business logic.
- **Service layer** — orchestrates domain objects and repositories to carry out business operations.
- **API layer** — thin FastAPI routes exposing the services over HTTP, with request/response validation via Pydantic schemas.

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Framework:** FastAPI
- **Database:** MongoDB (via Motor async driver), hosted on MongoDB Atlas
- **Validation:** Pydantic v2
- **Testing:** pytest (20 automated tests covering domain logic and API endpoints)
- **Containerization:** Docker
- **Deployment:** Render (auto-deploy from GitHub)
- **Dependency management:** Poetry

## 🚀 Running Locally

**Prerequisites:** Python 3.11, Poetry, and a MongoDB connection string (e.g. from MongoDB Atlas).

```bash
# 1. Clone the repository
git clone https://github.com/Rak5h17a/Lib_mgt_sys.git
cd Lib_mgt_sys/library-api

# 2. Install dependencies
poetry install

# 3. Create a .env file (see .env.example)
#    MONGODB_URL=your_mongodb_connection_string
#    DATABASE_NAME=library_db

# 4. Run the server
uvicorn app.main:app --reload
```

Then open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the API.

## 🧪 Running Tests

```bash
pytest
```

## 📌 Example Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/items/books` | Add a book |
| `GET`  | `/items/{item_id}` | Fetch an item |
| `POST` | `/members/students` | Register a student |
| `POST` | `/loans/borrow` | Borrow an item |
| `POST` | `/loans/{loan_id}/return` | Return an item |

## 📈 Possible Future Enhancements

- Authentication & role-based access (admin vs. member)
- A frontend UI (e.g. React) consuming the API
- Database transactions for multi-step operations