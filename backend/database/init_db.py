"""Database bootstrap that creates tables from SQLAlchemy models on app startup."""

from database.db import Base, engine
from database import models  # noqa: F401


def init_database():
    Base.metadata.create_all(bind=engine)
