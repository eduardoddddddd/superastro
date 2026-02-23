"""Dataclasses para datos astrológicos."""

from dataclasses import dataclass, field


@dataclass
class PlanetPosition:
    name: str
    longitude: float
    latitude: float
    speed: float
    sign: str
    degree_in_sign: float
    position_str: str
    retrograde: bool
    house: int


@dataclass
class Aspect:
    planet1: str
    planet2: str
    aspect_name: str
    exact_angle: float
    actual_angle: float
    orb: float


@dataclass
class ChartData:
    planets: list[PlanetPosition]
    cusps: list[float]
    ascendant: float
    mc: float
    aspects: list[Aspect]
    house_system: str
    jd: float


@dataclass
class TransitAspect:
    transit_planet: str
    natal_planet: str
    aspect_name: str
    orb: float
    is_applying: bool


@dataclass
class TransitData:
    natal_chart: ChartData
    transit_planets: list[PlanetPosition]
    transit_aspects: list[TransitAspect]
