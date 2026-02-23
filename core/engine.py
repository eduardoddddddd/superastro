"""Motor de cálculos astrológicos (Swiss Ephemeris)."""

import os

import swisseph as swe
from datetime import datetime
from zoneinfo import ZoneInfo

from core.models import PlanetPosition, Aspect, ChartData, TransitAspect, TransitData

EPHE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "data", "ephemeris")

SIGN_NAMES = [
    "Aries", "Tauro", "Géminis", "Cáncer",
    "Leo", "Virgo", "Libra", "Escorpio",
    "Sagitario", "Capricornio", "Acuario", "Piscis",
]

ASPECT_NAMES = {
    0: "Conjunción",
    60: "Sextil",
    90: "Cuadratura",
    120: "Trígono",
    180: "Oposición",
}

NATAL_ORBS = {0: 8, 60: 6, 90: 8, 120: 8, 180: 8}
TRANSIT_ORBS = {0: 3, 60: 2, 90: 3, 120: 3, 180: 3}

# Planetas para cada tipo de carta
PLANETS_HORARY = [
    swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS,
    swe.MARS, swe.JUPITER, swe.SATURN, swe.MEAN_NODE,
]
PLANETS_NATAL = [
    swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS,
    swe.MARS, swe.JUPITER, swe.SATURN,
    swe.URANUS, swe.NEPTUNE, swe.PLUTO, swe.MEAN_NODE,
]

PLANET_NAMES = {
    swe.SUN: "Sol", swe.MOON: "Luna",
    swe.MERCURY: "Mercurio", swe.VENUS: "Venus",
    swe.MARS: "Marte", swe.JUPITER: "Júpiter",
    swe.SATURN: "Saturno", swe.URANUS: "Urano",
    swe.NEPTUNE: "Neptuno", swe.PLUTO: "Plutón",
    swe.MEAN_NODE: "Nodo Norte",
}


_calc_flags = swe.FLG_SWIEPH


def _init_ephe():
    global _calc_flags
    if os.path.isdir(EPHE_PATH):
        swe.set_ephe_path(EPHE_PATH)
        # Test if ephemeris files actually work
        try:
            swe.calc_ut(2451545.0, swe.SUN, swe.FLG_SWIEPH)
            _calc_flags = swe.FLG_SWIEPH
        except swe.Error:
            _calc_flags = swe.FLG_MOSEPH
    else:
        _calc_flags = swe.FLG_MOSEPH


def _lon_to_sign(longitude):
    sign_index = int(longitude // 30)
    deg_in_sign = longitude - sign_index * 30
    return SIGN_NAMES[sign_index], deg_in_sign


def _assign_house(longitude: float, cusps: list) -> int:
    """Asigna la casa a un planeta comparando directamente con las cúspides.

    Más fiable que swe.house_pos() para planetas cercanos al ASC u otras
    cúspides, donde la función oficial puede devolver valores fuera de [1,12].

    cusps: lista de 12 longitudes eclípticas de cúspides (Casa 1 … Casa 12).
    """
    lon = longitude % 360.0
    for i in range(12):
        a = cusps[i] % 360.0
        b = cusps[(i + 1) % 12] % 360.0
        if a < b:
            # sector normal sin cruce de 0°/360°
            if a <= lon < b:
                return i + 1
        else:
            # sector que cruza 0°/360° (p.ej. cúspide en Piscis → siguiente en Aries)
            if lon >= a or lon < b:
                return i + 1
    return 1  # no debería llegar aquí


def _format_position(longitude):
    sign, deg_in_sign = _lon_to_sign(longitude)
    degrees = int(deg_in_sign)
    minutes = int((deg_in_sign - degrees) * 60)
    return f"{degrees:02d}°{minutes:02d}' {sign}"


def _angle_diff(a, b):
    diff = abs(a - b) % 360
    return min(diff, 360 - diff)


def local_to_utc(dt: datetime, timezone_str: str) -> datetime:
    """Convierte hora local a UTC usando zoneinfo."""
    tz = ZoneInfo(timezone_str)
    local_dt = dt.replace(tzinfo=tz)
    return local_dt.astimezone(ZoneInfo("UTC"))


def calculate_chart(dt: datetime, lat: float, lon: float,
                    house_system: str = "P", is_horary: bool = False) -> ChartData:
    """Calcula una carta astrológica.

    Args:
        dt: datetime en UTC
        lat, lon: coordenadas geográficas
        house_system: 'P' (Placidus) o 'R' (Regiomontanus)
        is_horary: si True, usa solo planetas tradicionales
    """
    _init_ephe()

    decimal_hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
    jd = swe.julday(dt.year, dt.month, dt.day, decimal_hour)

    cusps_tuple, ascmc = swe.houses(jd, lat, lon, house_system.encode())
    cusps = list(cusps_tuple)
    ascendant = ascmc[0]
    mc_val = ascmc[1]

    planet_ids = PLANETS_HORARY if is_horary else PLANETS_NATAL
    orbs = NATAL_ORBS

    planets = []
    for pid in planet_ids:
        result, _ = swe.calc_ut(jd, pid, _calc_flags)
        longitude = result[0]
        latitude = result[1]
        speed = result[3]
        sign, deg_in_sign = _lon_to_sign(longitude)
        house = _assign_house(longitude, cusps)
        planets.append(PlanetPosition(
            name=PLANET_NAMES[pid],
            longitude=longitude,
            latitude=latitude,
            speed=speed,
            sign=sign,
            degree_in_sign=deg_in_sign,
            position_str=_format_position(longitude),
            retrograde=speed < 0,
            house=house,
        ))

    aspects = _calculate_aspects(planets, orbs)

    swe.close()

    return ChartData(
        planets=planets,
        cusps=cusps,
        ascendant=ascendant,
        mc=mc_val,
        aspects=aspects,
        house_system=house_system,
        jd=jd,
    )


def _calculate_aspects(planets: list[PlanetPosition],
                       orbs: dict) -> list[Aspect]:
    aspects = []
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            diff = _angle_diff(planets[i].longitude, planets[j].longitude)
            for angle, max_orb in orbs.items():
                actual_orb = abs(diff - angle)
                if actual_orb <= max_orb:
                    aspects.append(Aspect(
                        planet1=planets[i].name,
                        planet2=planets[j].name,
                        aspect_name=ASPECT_NAMES[angle],
                        exact_angle=angle,
                        actual_angle=round(diff, 2),
                        orb=round(actual_orb, 2),
                    ))
                    break
    return aspects


def calculate_transits(natal_chart: ChartData,
                       transit_dt: datetime,
                       lat: float, lon: float) -> TransitData:
    """Calcula tránsitos sobre una carta natal."""
    _init_ephe()

    decimal_hour = transit_dt.hour + transit_dt.minute / 60.0 + transit_dt.second / 3600.0
    jd = swe.julday(transit_dt.year, transit_dt.month, transit_dt.day, decimal_hour)

    # Casas del momento del tránsito
    cusps_tuple, ascmc = swe.houses(jd, lat, lon, b'P')
    transit_cusps = list(cusps_tuple)

    transit_planets = []
    for pid in PLANETS_NATAL:
        result, _ = swe.calc_ut(jd, pid, _calc_flags)
        longitude = result[0]
        latitude = result[1]
        speed = result[3]
        sign, deg_in_sign = _lon_to_sign(longitude)
        house = _assign_house(longitude, transit_cusps)
        transit_planets.append(PlanetPosition(
            name=PLANET_NAMES[pid],
            longitude=longitude,
            latitude=latitude,
            speed=speed,
            sign=sign,
            degree_in_sign=deg_in_sign,
            position_str=_format_position(longitude),
            retrograde=speed < 0,
            house=house,
        ))

    # Aspectos cruzados: tránsito vs natal
    transit_aspects = []
    for tp in transit_planets:
        for np in natal_chart.planets:
            diff = _angle_diff(tp.longitude, np.longitude)
            for angle, max_orb in TRANSIT_ORBS.items():
                actual_orb = abs(diff - angle)
                if actual_orb <= max_orb:
                    # Determinar si es aplicativo
                    # Si el planeta de tránsito se mueve hacia el aspecto exacto
                    is_applying = _is_aspect_applying(
                        tp.longitude, tp.speed, np.longitude, angle)
                    transit_aspects.append(TransitAspect(
                        transit_planet=tp.name,
                        natal_planet=np.name,
                        aspect_name=ASPECT_NAMES[angle],
                        orb=round(actual_orb, 2),
                        is_applying=is_applying,
                    ))
                    break

    swe.close()

    return TransitData(
        natal_chart=natal_chart,
        transit_planets=transit_planets,
        transit_aspects=transit_aspects,
    )


def _is_aspect_applying(transit_lon, transit_speed, natal_lon, aspect_angle):
    """Determina si un aspecto de tránsito es aplicativo."""
    diff = (transit_lon - natal_lon) % 360
    if diff > 180:
        diff -= 360

    if aspect_angle == 0:
        target = 0
    elif aspect_angle == 180:
        target = 180 if diff > 0 else -180
    else:
        target = aspect_angle if abs(diff - aspect_angle) < abs(diff + aspect_angle) else -aspect_angle

    # Si el tránsito se acerca al ángulo exacto, es aplicativo
    current_dist = abs(abs(diff) - aspect_angle)
    future_diff = diff + transit_speed * 0.1  # pequeño avance
    future_dist = abs(abs(future_diff) - aspect_angle)

    return future_dist < current_dist
