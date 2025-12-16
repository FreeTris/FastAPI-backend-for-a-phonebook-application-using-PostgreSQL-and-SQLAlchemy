# Phonebook API (FastAPI)

A small backend API built with **FastAPI** and **PostgreSQL** to practice API design,
relational data modeling, and backend correctness.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- psycopg (Postgres driver)
- Uvicorn

## Features
- Health check endpoint
- Create users
- Create and list contacts
- Dependency-injected database sessions
- Relational data modeling using SQLAlchemy

## Design Notes
- The project uses PostgreSQL with SQLAlchemy to model relationships between users and contacts
- Database integrity is enforced at the data layer instead of relying on assumptions
- Authentication and additional CRUD endpoints are intentionally scoped out to focus on backend fundamentals

## Local Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload


