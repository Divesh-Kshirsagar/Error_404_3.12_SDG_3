"""
Database configuration and session management for SQLite
"""
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
from typing import Generator

# SQLite database URL (file-based)
DATABASE_URL = "sqlite:///./aarogyaqueue.db"

# Create engine with SQLite-specific settings
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # Allow multi-threaded access
)

def create_db_and_tables():
    """
    Create all tables in the database
    Called on application startup
    """
    SQLModel.metadata.create_all(engine)
    print("✅ Database tables created successfully")

def get_session() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI to get database session
    Usage: session: Session = Depends(get_session)
    """
    with Session(engine) as session:
        yield session

@contextmanager
def get_session_context() -> Generator[Session, None, None]:
    """
    Context manager for database session (for scripts)
    Usage: 
        with get_session_context() as session:
            # do database operations
    """
    with Session(engine) as session:
        yield session
        session.commit()
