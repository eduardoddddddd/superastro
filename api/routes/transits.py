"""Endpoints para tránsitos."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from core.engine import calculate_chart, calculate_transits, local_to_utc
from core.interpretations import interpret_transits
from core.charts_db import ChartsDatabase
import os

router = APIRouter()

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "data", "charts.db")


class TransitRequest(BaseModel):
    # Datos natales
    natal_year: int
    natal_month: int
    natal_day: int
    natal_hour: int
    natal_minute: int
    natal_lat: float
    natal_lon: float
    natal_timezone: str
    # Datos del tránsito
    transit_year: int
    transit_month: int
    transit_day: int
    transit_hour: int
    transit_minute: int
    transit_timezone: str


class TransitFromSavedRequest(BaseModel):
    chart_id: int
    transit_year: int
    transit_month: int
    transit_day: int
    transit_hour: int
    transit_minute: int
    transit_timezone: str


@router.post("/calculate")
async def calculate_transit(req: TransitRequest):
    try:
        # Calcular carta natal
        natal_dt_local = datetime(req.natal_year, req.natal_month, req.natal_day,
                                  req.natal_hour, req.natal_minute)
        natal_dt_utc = local_to_utc(natal_dt_local, req.natal_timezone)
        natal_chart = calculate_chart(natal_dt_utc, req.natal_lat, req.natal_lon)

        # Calcular tránsito
        transit_dt_local = datetime(req.transit_year, req.transit_month, req.transit_day,
                                    req.transit_hour, req.transit_minute)
        transit_dt_utc = local_to_utc(transit_dt_local, req.transit_timezone)
        transit_data = calculate_transits(natal_chart, transit_dt_utc,
                                          req.natal_lat, req.natal_lon)

        interpretations = interpret_transits(transit_data)

        return _format_transit_response(transit_data, interpretations)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calculate-from-saved")
async def calculate_transit_from_saved(req: TransitFromSavedRequest):
    try:
        db = ChartsDatabase(DB_PATH)
        data = db.get_chart(req.chart_id)
        db.close()

        if not data:
            raise HTTPException(status_code=404, detail="Carta no encontrada")

        natal_chart = data["chart"]
        lat = data["lat"]
        lon = data["lon"]

        transit_dt_local = datetime(req.transit_year, req.transit_month, req.transit_day,
                                    req.transit_hour, req.transit_minute)
        transit_dt_utc = local_to_utc(transit_dt_local, req.transit_timezone)
        transit_data = calculate_transits(natal_chart, transit_dt_utc, lat, lon)
        interpretations = interpret_transits(transit_data)

        return _format_transit_response(transit_data, interpretations)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _format_transit_response(transit_data, interpretations):
    transit_planets = []
    for p in transit_data.transit_planets:
        transit_planets.append({
            "name": p.name,
            "sign": p.sign,
            "degree_in_sign": round(p.degree_in_sign, 2),
            "house": p.house,
            "position_str": p.position_str,
            "retrograde": p.retrograde,
            "longitude": round(p.longitude, 4),
        })

    transit_aspects = []
    for ta in transit_data.transit_aspects:
        transit_aspects.append({
            "transit_planet": ta.transit_planet,
            "natal_planet": ta.natal_planet,
            "aspect_name": ta.aspect_name,
            "orb": ta.orb,
            "is_applying": ta.is_applying,
        })

    natal_planets = []
    for p in transit_data.natal_chart.planets:
        natal_planets.append({
            "name": p.name,
            "sign": p.sign,
            "degree_in_sign": round(p.degree_in_sign, 2),
            "house": p.house,
            "position_str": p.position_str,
            "retrograde": p.retrograde,
            "longitude": round(p.longitude, 4),
        })

    return {
        "success": True,
        "natal_planets": natal_planets,
        "natal_cusps": [round(c, 4) for c in transit_data.natal_chart.cusps],
        "natal_ascendant": round(transit_data.natal_chart.ascendant, 4),
        "natal_mc": round(transit_data.natal_chart.mc, 4),
        "natal_aspects": [
            {
                "planet1": a.planet1,
                "planet2": a.planet2,
                "aspect_name": a.aspect_name,
                "orb": a.orb,
                "exact_angle": a.exact_angle,
            }
            for a in transit_data.natal_chart.aspects
        ],
        "transit_planets": transit_planets,
        "transit_aspects": transit_aspects,
        "interpretations": interpretations,
    }
