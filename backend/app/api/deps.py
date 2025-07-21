from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    Dependency that provides a database session for each request.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()