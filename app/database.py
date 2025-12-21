from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use environment variable 
DATABASE_URL = os.getenv("DATABASE_URL")

# Don't create engine here!
engine = None
SessionLocal = None
Base = declarative_base()

def init_db():
    """Initialize the engine only when needed (lazy)."""
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,              # Helps to detect broken connections
            connect_args={"connect_timeout": 10}  # Wait longer for database to be ready
        )
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )

def get_db():
    init_db()  # This ensures engine is created only on first request
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()