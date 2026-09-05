"""
SQLAlchemy engine/session setup.

Why SQLite for dev with a Postgres-compatible schema: this is the "single
source of truth for pipeline state" described in Plan.md §5. Switching
DATABASE_URL to a Postgres connection string later is meant to be a config
change, not a rewrite (TechStack.md).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# SQLite needs this flag for use with FastAPI's threaded request handling;
# it's a no-op for Postgres, so it's safe to leave in for both.
connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()