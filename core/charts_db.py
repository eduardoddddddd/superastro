"""Base de datos SQLite para cartas guardadas."""

import os
import sqlite3
from dataclasses import dataclass
from typing import List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "data", "charts.db")


@dataclass
class SavedChart:
    id: int
    name: str
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str
    city_name: str
    created_at: str


class ChartsDatabase:

    def __init__(self, db_path: str = DB_PATH):
        self._db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS saved_charts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    birth_date TEXT NOT NULL,
                    birth_time TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    timezone TEXT NOT NULL,
                    city_name TEXT NOT NULL DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save(self, name: str, birth_date: str, birth_time: str,
             latitude: float, longitude: float, timezone: str,
             city_name: str = "") -> int:
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                """INSERT INTO saved_charts
                   (name, birth_date, birth_time, latitude, longitude, timezone, city_name)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (name, birth_date, birth_time, latitude, longitude, timezone, city_name))
            return cur.lastrowid

    def list_all(self) -> List[SavedChart]:
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM saved_charts ORDER BY created_at DESC").fetchall()
            return [SavedChart(**dict(r)) for r in rows]

    def get(self, chart_id: int) -> Optional[SavedChart]:
        with sqlite3.connect(self._db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM saved_charts WHERE id = ?", (chart_id,)).fetchone()
            return SavedChart(**dict(row)) if row else None

    def delete(self, chart_id: int) -> bool:
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                "DELETE FROM saved_charts WHERE id = ?", (chart_id,))
            return cur.rowcount > 0
