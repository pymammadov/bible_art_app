from __future__ import annotations

import sqlite3

from database.seed_data import populate_database

from .config import get_auto_seed_db, get_database_path

DB_PATH = get_database_path()


def initialize_db() -> None:
    """Create and seed the SQLite database if it doesn't exist yet."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        return

    if not get_auto_seed_db():
        raise RuntimeError(
            f"Database not found at {DB_PATH}. Set AUTO_SEED_DB=true for first deploy or provision the DB file manually."
        )

    populate_database(target_db_path=DB_PATH)


def get_connection() -> sqlite3.Connection:
    """Return a sqlite connection configured with Row objects."""
    initialize_db()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
