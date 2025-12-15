# Phonebook Backend (FastAPI)

A simple backend service built with FastAPI, SQLAlchemy, and PostgreSQL.

## Used Tech Stack
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- psycopg (Postgres driver)
- Uvicorn

## Features implemented in the Project
- Health check endpoint
- Create users
- SQLAlchemy models & schemas
- Dependency-injected DB sessions

## Local Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
