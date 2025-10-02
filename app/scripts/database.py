"""
This module contains the database connection setup for the FastAPI application.

It defines the database engine, the session maker, and a dependency function
to be used in FastAPI path operations to get a database session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Define the database URL for a local SQLite database file.
# The file will be created in the same directory as this script.
SQLALCHEMY_DATABASE_URL = "sqlite:///../recruitment_app.db"

# Create the SQLAlchemy engine.
# `connect_args` is needed only for SQLite to allow multi-threaded access.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class. Each instance of this class will be a database session.
# The class itself is not a session yet, but will create sessions when instantiated.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency to get a database session.

    This function creates a new database session for each request, handles
    exceptions, and ensures that the session is always closed after the
    request is finished, returning the connection to the connection pool.

    Yields:
        Session: The SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()