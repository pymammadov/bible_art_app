from __future__ import annotations

import sqlite3
from pathlib import Path

from database.seed_data import populate_database

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "bible_art.db"


def initialize_db() -> None:
    """Create and seed the SQLite database if it doesn't exist yet."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        return
    populate_database()


def get_connection() -> sqlite3.Connection:
    """Return a sqlite connection configured with Row objects."""
    initialize_db()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
