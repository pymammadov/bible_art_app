from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "bible_art.db"
SEED_SQL_PATH = BASE_DIR / "database" / "bible_art_seed.sql"


def initialize_db() -> None:
    """Create the SQLite database from seed SQL if it doesn't exist yet."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        return

    if not SEED_SQL_PATH.exists():
        raise FileNotFoundError(f"Missing seed SQL file at {SEED_SQL_PATH}")

    script = SEED_SQL_PATH.read_text(encoding="utf-8")
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(script)
        conn.commit()


def get_connection() -> sqlite3.Connection:
    """Return a sqlite connection configured with Row objects."""
    initialize_db()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
