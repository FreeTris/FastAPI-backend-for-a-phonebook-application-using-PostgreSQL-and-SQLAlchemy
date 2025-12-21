from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get the raw URL from Railway (it's postgres://...)
raw_database_url = os.getenv("DATABASE_URL")

if raw_database_url is None:
    raise ValueError("DATABASE_URL environment variable not set!")

# Railway gives postgres://... but SQLAlchemy needs postgresql://... for psycopg
# This fixes it automatically
if raw_database_url.startswith("postgres://"):
    DATABASE_URL = raw_database_url.replace("postgres://", "postgresql+psycopg://", 1)
else:
    DATABASE_URL = raw_database_url  # fallback, in case it's already correct

engine = None
SessionLocal = None
Base = declarative_base()

def init_db():
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10},  # ← Comma here!
        )
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )

def get_db():
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()