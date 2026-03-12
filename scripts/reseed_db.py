from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "bible_art.db"
SEED_SQL_PATH = BASE_DIR / "database" / "bible_art_seed.sql"


def reseed() -> None:
    if not SEED_SQL_PATH.exists():
        raise FileNotFoundError(f"Missing seed SQL file: {SEED_SQL_PATH}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    script = SEED_SQL_PATH.read_text(encoding="utf-8")
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(script)
        conn.commit()

    print(f"Reseeded database at {DB_PATH}")


if __name__ == "__main__":
    reseed()
