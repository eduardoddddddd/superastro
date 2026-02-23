"""Endpoints para búsqueda de ciudades."""

from fastapi import APIRouter, HTTPException, Query
from core.cities import CityDatabase
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "data", "cities.db")


@router.get("/search")
async def search_cities(q: str = Query(..., min_length=2)):
    try:
        db = CityDatabase(DB_PATH)
        results = db.search(q, limit=10)
        db.close()
        cities = []
        for r in results:
            cities.append({
                "name": r.name,
                "country": r.country_code,
                "lat": r.lat,
                "lon": r.lon,
                "timezone": r.timezone,
                "display": f"{r.name}, {r.country_code}",
            })
        return {"success": True, "cities": cities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
