# Blog API

A production-style REST API built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Alembic**. This project is part of my backend development journey, focusing on writing clean, scalable, and maintainable APIs.

## Features

* User registration
* User CRUD operations
* Password hashing
* PostgreSQL database integration
* SQLAlchemy ORM
* Alembic database migrations
* Pydantic request and response validation
* Environment variable configuration with `.env`
* Modular project structure

## Tech Stack

* Python 3
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* Passlib
* Uvicorn
* python-dotenv

## Project Structure

```
blog-api/
├── alembic/
├── app/
│   ├── routers/
│   ├── core/
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── .env
├── alembic.ini
└── requirements.txt
```

## Installation

```bash
git clone <repository-url>
cd blog-api

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file and add your database URL:

```env
DATABASE_URL=your_postgresql_database_url
```

## Run the Project

```bash
uvicorn app.main:app --reload
```

Open your browser:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

## Database Migrations

Create a migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

## Current Progress

* ✅ Project setup
* ✅ PostgreSQL connection
* ✅ SQLAlchemy models
* ✅ Alembic migrations
* ✅ User schemas
* ✅ User CRUD endpoints
* ✅ Password hashing
* 🚧 Authentication and authorization
* 🚧 Blog post endpoints
* 🚧 Testing
* 🚧 Docker
* 🚧 Redis

## Future Improvements

* JWT Authentication
* Login and protected routes
* Blog post management
* Comments
* Likes
* Pagination
* Search and filtering
* Docker support
* Redis caching
* Unit and integration tests

## Author

**Harshit Uniyal**

Backend Developer | Python | FastAPI
