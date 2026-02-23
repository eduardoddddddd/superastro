"""Endpoints para astrología horaria."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from core.engine import calculate_chart, local_to_utc
from core.interpretations import interpret_horary

router = APIRouter()


class HoraryRequest(BaseModel):
    question: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    lat: float
    lon: float
    timezone: str


@router.post("/calculate")
async def calculate_horary(req: HoraryRequest):
    try:
        dt_local = datetime(req.year, req.month, req.day, req.hour, req.minute)
        dt_utc = local_to_utc(dt_local, req.timezone)
        chart = calculate_chart(dt_utc, req.lat, req.lon,
                                house_system="R", is_horary=True)
        interpretations = interpret_horary(chart, req.question)

        planets_data = []
        for p in chart.planets:
            planets_data.append({
                "name": p.name,
                "sign": p.sign,
                "degree_in_sign": round(p.degree_in_sign, 2),
                "house": p.house,
                "position_str": p.position_str,
                "retrograde": p.retrograde,
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
            "question": req.question,
            "planets": planets_data,
            "cusps": [round(c, 4) for c in chart.cusps],
            "ascendant": round(chart.ascendant, 4),
            "mc": round(chart.mc, 4),
            "aspects": aspects_data,
            "house_system": "R",
            "interpretations": interpretations,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
