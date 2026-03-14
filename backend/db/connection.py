import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base

logger = logging.getLogger(__name__)

# Load environment variables (e.g., from .env)
load_dotenv()

# We prefer postgres, but allow a sqlite fallback if the environment doesn't have postgres running yet
# User requested PostgreSQL. Format: postgresql+psycopg2://user:password@host:port/dbname
_raw_url = os.getenv("DATABASE_URL", "")

# If DATABASE_URL is empty or looks like a bare postgres:// (dj-database-url format with no credentials),
# fall back to a local SQLite file so the backend can start in development without a Postgres instance.
if not _raw_url or _raw_url.strip() in ("", "postgres://", "postgresql://"):
    DATABASE_URL = "sqlite:///./price_intel.db"
    logger.info("DATABASE_URL not set — falling back to SQLite for SQLAlchemy price-history layer.")
else:
    DATABASE_URL = _raw_url

try:
    engine = create_engine(DATABASE_URL, echo=False)
except Exception as e:
    logger.warning(f"Failed to create database engine with '{DATABASE_URL}': {e}. Falling back to SQLite.")
    DATABASE_URL = "sqlite:///./price_intel.db"
    engine = create_engine(DATABASE_URL, echo=False)

# Create a scoped session factory for safe thread-local sessions
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    """
    Creates all tables in the database if they don't already exist.
    """
    logger.info(f"Initializing database using: {DATABASE_URL}")
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Generator to provide a transactional scope around a series of operations.
    Useful for dependency injection in FastAPI / Views.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
