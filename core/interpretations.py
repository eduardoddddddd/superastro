"""Dignidades, significados e interpretaciones astrológicas."""

from core.models import ChartData, TransitData
from core.transit_interpretations import build_transit_interpretation
from core.natal_interpretations import (
    build_natal_planet_text, build_asc_text,
    ASC_IN_SIGN, PLANET_IN_SIGN, PLANET_IN_HOUSE,
)

# ── Dignidades esenciales ─────────────────────────────────────────────────

DOMICILIO = {
    "Sol": ["Leo"],
    "Luna": ["Cáncer"],
    "Mercurio": ["Géminis", "Virgo"],
    "Venus": ["Tauro", "Libra"],
    "Marte": ["Aries", "Escorpio"],
    "Júpiter": ["Sagitario", "Piscis"],
    "Saturno": ["Capricornio", "Acuario"],
}

EXALTACION = {
    "Sol": "Aries",
    "Luna": "Tauro",
    "Mercurio": "Virgo",
    "Venus": "Piscis",
    "Marte": "Capricornio",
    "Júpiter": "Cáncer",
    "Saturno": "Libra",
}

DETRIMENTO = {
    "Sol": ["Acuario"],
    "Luna": ["Capricornio"],
    "Mercurio": ["Sagitario", "Piscis"],
    "Venus": ["Aries", "Escorpio"],
    "Marte": ["Tauro", "Libra"],
    "Júpiter": ["Géminis", "Virgo"],
    "Saturno": ["Cáncer", "Leo"],
}

CAIDA = {
    "Sol": "Libra",
    "Luna": "Escorpio",
    "Mercurio": "Piscis",
    "Venus": "Virgo",
    "Marte": "Cáncer",
    "Júpiter": "Capricornio",
    "Saturno": "Aries",
}


def get_dignity(planet, sign):
    if planet in DOMICILIO and sign in DOMICILIO[planet]:
        return "Domicilio"
    if planet in EXALTACION and EXALTACION[planet] == sign:
        return "Exaltación"
    if planet in DETRIMENTO and sign in DETRIMENTO[planet]:
        return "Detrimento"
    if planet in CAIDA and CAIDA[planet] == sign:
        return "Caída"
    return "Peregrino"


# ── Significados ──────────────────────────────────────────────────────────

HOUSE_MEANINGS = {
    1: "El consultante, su estado y apariencia",
    2: "Dinero y posesiones del consultante",
    3: "Hermanos, vecinos, viajes cortos, comunicaciones",
    4: "Hogar, familia, padre, bienes raíces, final del asunto",
    5: "Hijos, creatividad, romance, placeres, especulación",
    6: "Enfermedad, trabajo cotidiano, servicio, mascotas",
    7: "La otra persona, pareja, oponente, socio",
    8: "Muerte, herencias, dinero de otros, transformación",
    9: "Viajes largos, educación superior, religión, leyes",
    10: "Carrera, reputación, madre, autoridad",
    11: "Amigos, esperanzas, grupos, beneficios",
    12: "Enemigos ocultos, aislamiento, hospitales, auto-sabotaje",
}

ASPECT_MEANINGS = {
    "Conjunción": "Unión de energías, encuentro directo; puede ser favorable o tenso según los planetas",
    "Sextil": "Oportunidad que requiere esfuerzo; armonía moderada, cooperación",
    "Cuadratura": "Tensión, obstáculo, conflicto; requiere acción para resolver",
    "Trígono": "Flujo fácil, armonía, resultado favorable sin mucho esfuerzo",
    "Oposición": "Confrontación, polaridad; necesidad de equilibrio entre dos fuerzas",
}

PLANET_MEANINGS = {
    "Sol": "Autoridad, poder, figuras paternas, vitalidad, éxito",
    "Luna": "Emociones, lo cotidiano, flujo de eventos, la madre",
    "Mercurio": "Comunicación, comercio, documentos, viajes cortos, mensajes",
    "Venus": "Amor, armonía, belleza, dinero, valores",
    "Marte": "Acción, conflicto, cirugía, energía, prisa",
    "Júpiter": "Expansión, suerte, abundancia, jueces, maestros",
    "Saturno": "Restricción, demoras, tiempo, estructuras, disciplina",
    "Urano": "Cambios repentinos, innovación, rebeldía, tecnología",
    "Neptuno": "Ilusión, espiritualidad, confusión, arte, sacrificio",
    "Plutón": "Transformación profunda, poder oculto, regeneración",
    "Nodo Norte": "Destino, crecimiento, dirección kármica",
}

DIGNITY_DESCRIPTIONS = {
    "Domicilio": "Fuerte y cómodo, actúa con plena capacidad",
    "Exaltación": "Muy fuerte, honrado, en su mejor expresión",
    "Detrimento": "Debilitado, incómodo, con dificultades para actuar",
    "Caída": "Muy débil, humillado, en su peor condición",
    "Peregrino": "Sin dignidad especial, depende del contexto",
}

ASPECT_ANGLES = [0, 60, 90, 120, 180]
ASPECT_ORBS_TIGHT = {0: 8, 60: 6, 90: 8, 120: 8, 180: 8}


def _is_void_of_course(moon, planets):
    """Detecta si la Luna está vacía de curso."""
    moon_lon = moon.longitude
    moon_sign_index = int(moon_lon // 30)
    degrees_left_in_sign = 30 - (moon_lon - moon_sign_index * 30)

    has_applying_aspect = False
    for p in planets:
        if p.name in ("Luna", "Nodo Norte"):
            continue
        p_lon = p.longitude
        diff = abs(moon_lon - p_lon) % 360
        diff = min(diff, 360 - diff)
        for angle in ASPECT_ANGLES:
            orb = ASPECT_ORBS_TIGHT[angle]
            separation = abs(diff - angle)
            if separation <= orb / 2:
                has_applying_aspect = True
                break
        if has_applying_aspect:
            break

    return not has_applying_aspect and degrees_left_in_sign < 15


# ── Funciones de interpretación ───────────────────────────────────────────

def interpret_natal(chart: ChartData) -> list[tuple[str, str]]:
    """Interpretación detallada de una carta natal."""
    sections = []

    # ── Ascendente ────────────────────────────────────────────────────────
    from core.natal_interpretations import build_asc_text, ASC_IN_SIGN
    import math
    asc_sign_index = int(chart.ascendant // 30) % 12
    SIGN_ORDER = [
        "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo",
        "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis",
    ]
    asc_sign = SIGN_ORDER[asc_sign_index]
    sections.append(("Ascendente en " + asc_sign, build_asc_text(asc_sign)))

    # ── Un bloque por planeta ─────────────────────────────────────────────
    for p in chart.planets:
        dignity = get_dignity(p.name, p.sign)
        # Aspectos que involucran a este planeta
        planet_aspects = [
            a for a in chart.aspects
            if a.planet1 == p.name or a.planet2 == p.name
        ]
        text = build_natal_planet_text(
            planet_name=p.name,
            sign=p.sign,
            house=p.house,
            dignity=dignity,
            retrograde=p.retrograde,
            aspects=planet_aspects,
        )
        title = f"{p.name} en {p.sign} — Casa {p.house}"
        if p.retrograde:
            title += " ℞"
        sections.append((title, text))

    return sections


def interpret_transits(data: TransitData) -> list[tuple[str, str]]:
    """Interpretación detallada de tránsitos sobre carta natal."""
    sections = []

    # Mapas de acceso rápido por nombre de planeta
    natal_map = {p.name: p for p in data.natal_chart.planets}
    transit_map = {p.name: p for p in data.transit_planets}

    if data.transit_aspects:
        applying = [a for a in data.transit_aspects if a.is_applying]
        separating = [a for a in data.transit_aspects if not a.is_applying]

        if applying:
            blocks = []
            for a in applying:
                natal_p = natal_map.get(a.natal_planet)
                transit_p = transit_map.get(a.transit_planet)
                natal_house = natal_p.house if natal_p else 1
                is_retro = transit_p.retrograde if transit_p else False

                header = (f"{a.transit_planet} {a.aspect_name} {a.natal_planet} "
                          f"(orbe {a.orb}°) — APLICATIVO")
                body = build_transit_interpretation(
                    a.transit_planet, a.natal_planet,
                    a.aspect_name, natal_house, is_retro,
                )
                blocks.append(f"[b]{header}[/b]\n{body}")
            sections.append(("Aspectos aplicativos — Interpretación",
                             "\n\n──────────────────────────────\n\n".join(blocks)))

        if separating:
            blocks = []
            for a in separating:
                natal_p = natal_map.get(a.natal_planet)
                transit_p = transit_map.get(a.transit_planet)
                natal_house = natal_p.house if natal_p else 1
                is_retro = transit_p.retrograde if transit_p else False

                header = (f"{a.transit_planet} {a.aspect_name} {a.natal_planet} "
                          f"(orbe {a.orb}°) — separativo")
                body = build_transit_interpretation(
                    a.transit_planet, a.natal_planet,
                    a.aspect_name, natal_house, is_retro,
                )
                blocks.append(f"[b]{header}[/b]\n{body}")
            sections.append(("Aspectos separativos — Interpretación",
                             "\n\n──────────────────────────────\n\n".join(blocks)))
    else:
        sections.append(("Aspectos de tránsito",
                         "  No se encontraron aspectos significativos."))

    # Dignidades de planetas en tránsito
    lines = []
    for p in data.transit_planets:
        dignity = get_dignity(p.name, p.sign)
        desc = DIGNITY_DESCRIPTIONS[dignity]
        line = f"  {p.name} en {p.sign}: {dignity} — {desc}"
        if p.retrograde:
            line += " [RETRÓGRADO]"
        lines.append(line)
    sections.append(("Estado de planetas en tránsito", "\n".join(lines)))

    return sections



# ── Tablas para horaria ───────────────────────────────────────────────────────

# Regentes tradicionales por signo (sin planetas modernos)
_TRADITIONAL_RULERS: dict[str, str] = {
    "Aries": "Marte",       "Tauro": "Venus",     "Géminis": "Mercurio",
    "Cáncer": "Luna",       "Leo": "Sol",         "Virgo": "Mercurio",
    "Libra": "Venus",       "Escorpio": "Marte",  "Sagitario": "Júpiter",
    "Capricornio": "Saturno", "Acuario": "Saturno", "Piscis": "Júpiter",
}

_SIGN_ORDER_HORARY = [
    "Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo",
    "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis",
]

# Signification de casas para preguntas frecuentes
_QUESTION_HOUSES: dict[str, dict] = {
    "amor/relación/pareja": {
        "casa_quesitado": 7,
        "guia": "La Casa 7 representa a la pareja o la persona preguntada. "
                "El regente de Casa 7 es el significador del otro. "
                "Si el regente de Casa 1 y el de Casa 7 tienen aspecto aplicativo, "
                "la relación puede desarrollarse. La Venus y la Luna aportan información "
                "sobre el flujo afectivo.",
    },
    "trabajo/empleo/carrera": {
        "casa_quesitado": 10,
        "guia": "La Casa 10 rige la carrera y el reconocimiento. "
                "La Casa 6 rige el empleo concreto y las condiciones laborales. "
                "Un aspecto del regente de Casa 1 al regente de Casa 10 o 6 "
                "indica movimiento en la dirección consultada.",
    },
    "dinero/finanzas/préstamo": {
        "casa_quesitado": 2,
        "guia": "La Casa 2 rige el dinero propio. La Casa 8 rige el dinero ajeno, "
                "los préstamos y las herencias. Saturno en Casa 2 puede indicar "
                "restricción o demora financiera.",
    },
    "salud/enfermedad": {
        "casa_quesitado": 6,
        "guia": "La Casa 6 rige la enfermedad y el estado de salud general. "
                "La Casa 1 y su regente representan el cuerpo del consultante. "
                "Marte indica inflamación; Saturno, enfermedades crónicas o cólicos; "
                "Mercurio, los nervios; Luna, los fluidos y ciclos.",
    },
    "viaje": {
        "casa_quesitado": 9,
        "guia": "La Casa 9 rige los viajes largos. La Casa 3 rige los viajes cortos. "
                "Saturno afflicto en la Casa 9 puede indicar obstáculos. "
                "Júpiter favorable sugiere viaje exitoso.",
    },
    "compra/venta/propiedad": {
        "casa_quesitado": 4,
        "guia": "La Casa 4 rige los bienes inmuebles y el final de los asuntos. "
                "La Casa 7 representa al vendedor/comprador. Un aspecto entre los "
                "regentes de Casa 1 y Casa 4 indica que la operación puede concretarse.",
    },
    "hijo/embarazo": {
        "casa_quesitado": 5,
        "guia": "La Casa 5 rige los hijos y el embarazo. La Luna es muy importante "
                "como co-significadora de la fertilidad. Júpiter en Casa 5 es muy "
                "favorable. Saturno puede indicar demora o dificultad.",
    },
    "litigio/juicio/legal": {
        "casa_quesitado": 7,
        "guia": "La Casa 7 rige al oponente en el litigio. La Casa 10 representa "
                "al juez o la autoridad. Si el regente de Casa 1 está más fuerte "
                "y dignificado que el de Casa 7, el consultante lleva ventaja.",
    },
}


def _get_sign_for_cusp(longitude: float) -> str:
    """Devuelve el signo del zodíaco para una longitud eclíptica."""
    idx = int(longitude // 30) % 12
    return _SIGN_ORDER_HORARY[idx]


def _get_house_ruler(cusp_lon: float) -> str:
    """Devuelve el regente tradicional del signo en esa cúspide."""
    sign = _get_sign_for_cusp(cusp_lon)
    return _TRADITIONAL_RULERS[sign]


def _check_combustion(planet_name: str, planets: list) -> bool:
    """Comprueba si un planeta está combust (a menos de 8° del Sol)."""
    if planet_name in ("Sol", "Luna"):
        return False
    sol = next((p for p in planets if p.name == "Sol"), None)
    target = next((p for p in planets if p.name == planet_name), None)
    if not sol or not target:
        return False
    diff = abs(sol.longitude - target.longitude) % 360
    diff = min(diff, 360 - diff)
    return diff < 8.0


def _check_reception(p1_name: str, p1_sign: str, p2_name: str, p2_sign: str) -> str:
    """Devuelve nota de recepción mutua si existe."""
    r1 = _TRADITIONAL_RULERS.get(p1_sign)
    r2 = _TRADITIONAL_RULERS.get(p2_sign)
    if r1 == p2_name and r2 == p1_name:
        return f"Recepción mutua entre {p1_name} y {p2_name}: cada uno está en el signo del otro, lo que facilita la negociación y el acuerdo."
    if r1 == p2_name:
        return f"{p1_name} está en el signo regido por {p2_name}, lo que indica que {p1_name} busca o necesita a {p2_name}."
    if r2 == p1_name:
        return f"{p2_name} está en el signo regido por {p1_name}, lo que indica que {p2_name} busca o necesita a {p1_name}."
    return ""


def interpret_horary(chart: ChartData, question: str = "") -> list[tuple[str, str]]:
    """Interpretación detallada de una carta horaria según reglas tradicionales."""
    sections = []
    planets_map = {p.name: p for p in chart.planets}

    # ── 1. SIGNIFICADORES ─────────────────────────────────────────────────
    lord1_name = _get_house_ruler(chart.cusps[0])
    lord1 = planets_map.get(lord1_name)
    lord1_sign = _get_sign_for_cusp(chart.cusps[0])
    moon = planets_map.get("Luna")

    lines = []
    lines.append(f"  Ascendente en {lord1_sign}")
    lines.append(f"  Regente de Casa 1 (significador del consultante): {lord1_name}")
    if lord1:
        dig1 = get_dignity(lord1_name, lord1.sign)
        retro1 = " — RETRÓGRADO (el consultante puede cambiar de opinión o el asunto puede retroceder)" if lord1.retrograde else ""
        comb1 = " — COMBUST (el consultante está debilitado, no ve bien la situación)" if _check_combustion(lord1_name, chart.planets) else ""
        lines.append(f"  {lord1_name} está en {lord1.sign}, Casa {lord1.house}")
        lines.append(f"  Dignidad del significador: {dig1} — {DIGNITY_DESCRIPTIONS[dig1]}{retro1}{comb1}")
    if moon:
        dig_moon = get_dignity("Luna", moon.sign)
        voc = _is_void_of_course(moon, chart.planets)
        lines.append(f"  Luna (co-significadora del consultante y del flujo del asunto): en {moon.sign}, Casa {moon.house}")
        lines.append(f"  Dignidad lunar: {dig_moon}{' — VACÍA DE CURSO ⚠' if voc else ''}")
    sections.append(("Significadores del consultante", "\n".join(lines)))

    # ── 2. ESTADO DE LA LUNA ─────────────────────────────────────────────
    if moon:
        voc = _is_void_of_course(moon, chart.planets)
        lines = []
        if voc:
            lines.append("  ⚠ LUNA VACÍA DE CURSO")
            lines.append("  La Luna abandona su signo actual sin perfeccionar ningún aspecto.")
            lines.append("  Regla tradicional: 'Nada saldrá de este asunto' o el resultado")
            lines.append("  será diferente a lo esperado. Hay que retrasar las decisiones importantes.")
        else:
            # Buscar el próximo aspecto de la Luna
            applying_moon = [
                a for a in chart.aspects
                if (a.planet1 == "Luna" or a.planet2 == "Luna")
            ]
            if applying_moon:
                next_asp = sorted(applying_moon, key=lambda a: a.orb)[0]
                other = next_asp.planet2 if next_asp.planet1 == "Luna" else next_asp.planet1
                lines.append(f"  Luna activa — próximo aspecto: {next_asp.aspect_name} con {other} (orbe {next_asp.orb}°)")
                asp_meaning = ASPECT_MEANINGS.get(next_asp.aspect_name, "")
                if asp_meaning:
                    lines.append(f"  Significado: {asp_meaning}")
                lines.append(f"  La Luna indica el flujo del asunto hacia {other}: {PLANET_MEANINGS.get(other, '')}")
            else:
                lines.append("  Luna activa pero sin aspectos claros en las próximas horas.")
        sections.append(("Estado de la Luna", "\n".join(lines)))

    # ── 3. ANÁLISIS POR CASAS ────────────────────────────────────────────
    lines = []
    for i in range(12):
        cusp_lon = chart.cusps[i]
        sign = _get_sign_for_cusp(cusp_lon)
        ruler = _get_house_ruler(cusp_lon)
        ruler_planet = planets_map.get(ruler)
        house_meaning = HOUSE_MEANINGS.get(i + 1, "")
        planeta_en_casa = [p for p in chart.planets if p.house == i + 1 and p.name not in ("Sol",)]

        status = f"  Casa {i+1} ({house_meaning}): regida por {ruler} en {sign}"
        if ruler_planet:
            dig = get_dignity(ruler, ruler_planet.sign)
            status += f" — {ruler} en {ruler_planet.sign} (Casa {ruler_planet.house}, {dig})"
            if ruler_planet.retrograde:
                status += " [R]"
        if planeta_en_casa:
            nombres = ", ".join(p.name for p in planeta_en_casa)
            status += f" | Planetas en casa: {nombres}"
        lines.append(status)
    sections.append(("Regentes de casas y posiciones", "\n".join(lines)))

    # ── 4. DIGNIDADES Y ESTADOS ──────────────────────────────────────────
    lines = []
    for p in chart.planets:
        dignity = get_dignity(p.name, p.sign)
        desc = DIGNITY_DESCRIPTIONS[dignity]
        line = f"  {p.name} en {p.sign}: {dignity} — {desc}"
        if p.retrograde:
            line += " [RETRÓGRADO]"
        if _check_combustion(p.name, chart.planets):
            line += " [COMBUST — muy debilitado]"
        lines.append(line)
    sections.append(("Dignidades y estados planetarios", "\n".join(lines)))

    # ── 5. ASPECTOS CON INTERPRETACIÓN ──────────────────────────────────
    if chart.aspects:
        lines = []
        for a in chart.aspects:
            p1 = planets_map.get(a.planet1)
            p2 = planets_map.get(a.planet2)
            meaning = ASPECT_MEANINGS.get(a.aspect_name, "")
            line = f"  {a.planet1} {a.aspect_name} {a.planet2} (orbe {a.orb}°)"
            line += f"\n    → {meaning}"
            # Recepción
            if p1 and p2:
                rec = _check_reception(a.planet1, p1.sign, a.planet2, p2.sign)
                if rec:
                    line += f"\n    ★ {rec}"
            lines.append(line)
        sections.append(("Aspectos con interpretación", "\n".join(lines)))

    # ── 6. ANÁLISIS DE PERFECCIÓN ────────────────────────────────────────
    # Aspecto aplicativo entre Lord 1 y cualquier otro significador de casa
    lines = []
    lord1_aspects = [
        a for a in chart.aspects
        if (a.planet1 == lord1_name or a.planet2 == lord1_name)
    ]
    if lord1_aspects:
        applying = [a for a in lord1_aspects if a.orb <= 5.0]  # orbe estrecho = más activo
        if applying:
            best = sorted(applying, key=lambda a: a.orb)[0]
            other = best.planet2 if best.planet1 == lord1_name else best.planet1
            other_planet = planets_map.get(other)
            lines.append(f"  El significador principal ({lord1_name}) forma un {best.aspect_name}")
            lines.append(f"  con {other} (orbe {best.orb}°).")
            lines.append(f"  {other} rige la Casa {other_planet.house if other_planet else '?'}: "
                         f"{HOUSE_MEANINGS.get(other_planet.house if other_planet else 0, '')}")
            asp_meaning = ASPECT_MEANINGS.get(best.aspect_name, "")
            lines.append(f"  Naturaleza del aspecto: {asp_meaning}")
            if best.aspect_name in ("Trígono", "Sextil", "Conjunción"):
                lines.append("  ✓ Aspecto favorable: indica posibilidad de que el asunto se resuelva positivamente.")
            elif best.aspect_name in ("Cuadratura", "Oposición"):
                lines.append("  ✗ Aspecto tenso: el asunto puede resolverse pero con obstáculos, conflicto o compromiso.")
        else:
            lines.append(f"  {lord1_name} no forma aspectos de orbe estrecho (<5°) en este momento.")
            lines.append("  El asunto puede estar en espera o no hay movimiento inmediato.")
    else:
        lines.append(f"  {lord1_name} no aspecto a otros planetas en esta carta.")
        lines.append("  Sin perfección clara: el asunto puede no tener resolución en el corto plazo.")

    # Luna aplicativa a Lord 1 o a planetas importantes
    if moon:
        moon_to_lord1 = [
            a for a in chart.aspects
            if (a.planet1 == "Luna" and a.planet2 == lord1_name) or
               (a.planet2 == "Luna" and a.planet1 == lord1_name)
        ]
        if moon_to_lord1:
            ma = moon_to_lord1[0]
            lines.append(f"  La Luna forma un {ma.aspect_name} con {lord1_name} (orbe {ma.orb}°).")
            lines.append("  La Luna refuerza el papel del consultante como actor principal del asunto.")

    sections.append(("Análisis de perfección (¿se concretará?)", "\n".join(lines)))

    # ── 7. GUÍA DE LECTURA ADAPTADA ──────────────────────────────────────
    guide_lines = [
        "  PASOS PARA LEER ESTA CARTA HORARIA:",
        "",
        f"  1. Tu significador es {lord1_name} (regente de Casa 1).",
        f"     Estado actual: ver sección 'Dignidades y estados'.",
        "",
        "  2. Identifica la casa que rige tu pregunta:",
        "     • Amor/pareja → Casa 7  • Trabajo/carrera → Casa 10  • Dinero → Casa 2",
        "     • Salud → Casa 6        • Hijos → Casa 5              • Viaje largo → Casa 9",
        "     • Hermanos → Casa 3     • Hogar/propiedades → Casa 4  • Amigos → Casa 11",
        "",
        "  3. Encuentra el regente de esa casa y observa si hay aspecto aplicativo",
        f"     con {lord1_name} o con la Luna.",
        "",
        "  4. Reglas básicas de resultado:",
        "     ✓ Aspecto aplicativo benigno (trígono/sextil): SÍ, el asunto avanza bien.",
        "     ✓ Conjunción (según planetas): SÍ con fuerza.",
        "     ✗ Cuadratura/oposición: SÍ pero con obstáculos o conflicto.",
        "     ✗ Sin aspecto: NO o resultado incierto.",
        "     ✗ Luna vacía de curso: NO o resultado inesperado.",
        "",
        "  5. Un significador RETRÓGRADO puede indicar que el consultante",
        "     cambiará de opinión, o que el asunto volverá a plantearse.",
        "",
        "  6. Un significador COMBUST está muy debilitado y puede indicar",
        "     que la persona no tiene poder real sobre el asunto.",
        "",
        "  7. La Casa 4 (su regente y planetas en ella) describe el final del asunto.",
    ]
    sections.append(("Guía de lectura tradicional", "\n".join(guide_lines)))

    return sections
