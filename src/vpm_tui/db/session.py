"""Database session management."""

from sqlalchemy.orm import sessionmaker

from vpm_tui.db.engine import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
