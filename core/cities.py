"""Búsqueda de ciudades usando SQLite + FTS5."""

import os
import sqlite3
from dataclasses import dataclass


@dataclass
class City:
    name: str
    country_code: str
    lat: float
    lon: float
    timezone: str
    population: int


class CityDatabase:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "cities.db"
            )
        self._db_path = db_path
        self._conn = None

    def _connect(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path)
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def is_available(self) -> bool:
        return os.path.isfile(self._db_path)

    def search(self, query: str, limit: int = 10) -> list[City]:
        if not query or not self.is_available():
            return []

        conn = self._connect()
        # FTS5 prefix search
        fts_query = query.strip() + "*"
        try:
            rows = conn.execute(
                """SELECT c.name, c.country_code, c.latitude, c.longitude,
                          c.timezone, c.population
                   FROM cities_fts f
                   JOIN cities c ON c.rowid = f.rowid
                   WHERE cities_fts MATCH ?
                   ORDER BY c.population DESC
                   LIMIT ?""",
                (fts_query, limit)
            ).fetchall()
        except sqlite3.OperationalError:
            # Fallback to LIKE if FTS fails
            rows = conn.execute(
                """SELECT name, country_code, latitude, longitude,
                          timezone, population
                   FROM cities
                   WHERE name LIKE ?
                   ORDER BY population DESC
                   LIMIT ?""",
                (query.strip() + "%", limit)
            ).fetchall()

        return [
            City(
                name=r[0], country_code=r[1],
                lat=r[2], lon=r[3],
                timezone=r[4], population=r[5]
            )
            for r in rows
        ]
