"""Endpoints para carta natal."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from core.engine import calculate_chart, local_to_utc
from core.interpretations import interpret_natal
from core.charts_db import ChartsDatabase
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "data", "charts.db")


class NatalRequest(BaseModel):
    name: str = ""
    year: int
    month: int
    day: int
    hour: int
    minute: int
    lat: float
    lon: float
    timezone: str
    city_name: str = ""
    house_system: str = "P"


@router.post("/calculate")
async def calculate_natal(req: NatalRequest):
    try:
        dt_local = datetime(req.year, req.month, req.day, req.hour, req.minute)
        dt_utc = local_to_utc(dt_local, req.timezone)
        chart = calculate_chart(dt_utc, req.lat, req.lon,
                                house_system=req.house_system, is_horary=False)
        interpretations = interpret_natal(chart)
        return _format_chart_response(chart, interpretations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
async def save_chart(req: NatalRequest):
    try:
        birth_date = f"{req.year:04d}-{req.month:02d}-{req.day:02d}"
        birth_time = f"{req.hour:02d}:{req.minute:02d}"
        db = ChartsDatabase(DB_PATH)
        chart_id = db.save(
            name=req.name,
            birth_date=birth_date,
            birth_time=birth_time,
            latitude=req.lat,
            longitude=req.lon,
            timezone=req.timezone,
            city_name=req.city_name,
        )
        return {"success": True, "id": chart_id, "message": f"Carta de {req.name} guardada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_charts():
    try:
        db = ChartsDatabase(DB_PATH)
        charts = db.list_all()
        result = []
        for c in charts:
            result.append({
                "id": c.id,
                "name": c.name,
                "birth_date": c.birth_date,
                "birth_time": c.birth_time,
                "city_name": c.city_name,
                "timezone": c.timezone,
            })
        return {"success": True, "charts": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/load/{chart_id}")
async def load_chart(chart_id: int):
    try:
        db = ChartsDatabase(DB_PATH)
        saved = db.get(chart_id)
        if not saved:
            raise HTTPException(status_code=404, detail="Carta no encontrada")

        year, month, day = saved.birth_date.split("-")
        hour, minute = saved.birth_time.split(":")
        dt_local = datetime(int(year), int(month), int(day), int(hour), int(minute))
        dt_utc = local_to_utc(dt_local, saved.timezone)
        chart = calculate_chart(dt_utc, saved.latitude, saved.longitude,
                                house_system="P", is_horary=False)
        interpretations = interpret_natal(chart)

        response = _format_chart_response(chart, interpretations)
        response["meta"] = {
            "id": saved.id,
            "name": saved.name,
            "birth_date": saved.birth_date,
            "birth_time": saved.birth_time,
            "lat": saved.latitude,
            "lon": saved.longitude,
            "timezone": saved.timezone,
            "city_name": saved.city_name,
        }
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{chart_id}")
async def delete_chart(chart_id: int):
    try:
        db = ChartsDatabase(DB_PATH)
        ok = db.delete(chart_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Carta no encontrada")
        return {"success": True, "message": "Carta eliminada"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _format_chart_response(chart, interpretations):
    planets_data = []
    for p in chart.planets:
        planets_data.append({
            "name": p.name,
            "sign": p.sign,
            "degree_in_sign": round(p.degree_in_sign, 2),
            "house": p.house,
            "position_str": p.position_str,
            "retrograde": p.retrograde,
            "speed": round(p.speed, 4),
            "longitude": round(p.longitude, 4),
        })

    aspects_data = []
    for a in chart.aspects:
        aspects_data.append({
            "planet1": a.planet1,
            "planet2": a.planet2,
            "aspect_name": a.aspect_name,
            "orb": a.orb,
            "exact_angle": a.exact_angle,
        })

    return {
        "success": True,
        "planets": planets_data,
        "cusps": [round(c, 4) for c in chart.cusps],
        "ascendant": round(chart.ascendant, 4),
        "mc": round(chart.mc, 4),
        "aspects": aspects_data,
        "house_system": chart.house_system,
        "jd": chart.jd,
        "interpretations": interpretations,
    }
