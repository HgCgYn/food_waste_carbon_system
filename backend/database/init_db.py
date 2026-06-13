"""Database bootstrap that creates tables and seeds food factors on startup."""

from pathlib import Path

from database.db import Base, engine
from database import models  # noqa: F401


SEED_SQL_PATH = Path(__file__).resolve().parents[1] / "sql" / "init.sql"


def init_database():
    Base.metadata.create_all(bind=engine)
    if not SEED_SQL_PATH.exists():
        return

    seed_sql = SEED_SQL_PATH.read_text(encoding="utf-8")
    raw_connection = engine.raw_connection()
    try:
        with raw_connection.cursor() as cursor:
            cursor.execute(seed_sql)
        raw_connection.commit()
    finally:
        raw_connection.close()
