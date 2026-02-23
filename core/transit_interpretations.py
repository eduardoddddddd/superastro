"""Interpretaciones detalladas de tránsitos planetarios.

Estructura:
- TRANSIT_BASE[(planeta_transito, planeta_natal)] -> texto base (3-5 frases)
- ASPECT_MODIFIER[aspecto] -> modificador por tipo de aspecto
- HOUSE_MODIFIER[casa] -> modificador por casa natal del planeta afectado
- RETROGRADE_NOTE -> nota cuando el planeta en tránsito es retrógrado
- build_transit_interpretation() -> ensambla el texto completo
"""

from __future__ import annotations

# ── Planetas y sus significados base (para fallback genérico) ─────────────
_PLANET_THEMES = {
    "Sol":        "identidad, vitalidad, propósito de vida y reconocimiento",
    "Luna":       "emociones, instintos, vida cotidiana y necesidades de seguridad",
    "Mercurio":   "mente, comunicación, aprendizaje y relaciones cotidianas",
    "Venus":      "amor, valores, placer estético, dinero y relaciones afectivas",
    "Marte":      "energía, deseo, iniciativa, conflicto y sexualidad",
    "Júpiter":    "expansión, confianza, abundancia, filosofía y crecimiento",
    "Saturno":    "estructura, limitación, responsabilidad, tiempo y madurez",
    "Urano":      "cambio súbito, originalidad, revolución y despertar",
    "Neptuno":    "espiritualidad, ilusión, disuelve fronteras, arte y sacrificio",
    "Plutón":     "transformación profunda, poder, muerte simbólica y regeneración",
    "Nodo Norte": "dirección kármica, crecimiento del alma y destino evolutivo",
}

# ── Modificadores por tipo de aspecto ─────────────────────────────────────

ASPECT_MODIFIER: dict[str, str] = {
    "Conjunción": (
        "La conjunción fusiona directamente estas dos energías en el mismo punto "
        "del cielo: los temas se manifiestan con intensidad máxima y no hay matiz "
        "armónico ni tensional que los filtre. Todo depende de la naturaleza de "
        "los planetas implicados — si son complementarios, el encuentro es "
        "poderoso y creativo; si son discordantes, la fusión puede resultar "
        "abrumadora y requerir integración consciente."
    ),
    "Trígono": (
        "El trígono facilita este tránsito: las energías fluyen sin resistencia "
        "significativa, ofreciendo oportunidades que llegan de forma natural y "
        "casi sin esfuerzo consciente. El riesgo del trígono es la pasividad — "
        "la facilidad puede hacer que no se aproveche plenamente el potencial "
        "disponible. Es un momento para expandir con confianza."
    ),
    "Sextil": (
        "El sextil abre una ventana de oportunidad real, pero que requiere acción "
        "deliberada para aprovecharse. A diferencia del trígono, la energía "
        "cooperativa no actúa sola; hay que dar un paso hacia ella. Es un "
        "momento favorable para iniciar proyectos, conversaciones o cambios "
        "relacionados con las áreas que estos planetas gobiernan."
    ),
    "Cuadratura": (
        "La cuadratura introduce tensión, fricción y conflicto entre las "
        "energías de los dos planetas. Esta presión no es necesariamente negativa "
        "— a menudo es el motor que impulsa el crecimiento — pero exige trabajo "
        "activo para resolver los obstáculos. Los temas se presentan como "
        "desafíos que demandan decisión y esfuerzo; ignorarlos no los hace "
        "desaparecer sino que los intensifica."
    ),
    "Oposición": (
        "La oposición polariza las energías entre el planeta en tránsito y el "
        "planeta natal, creando una tensión que frecuentemente se proyecta hacia "
        "el exterior: en relaciones, en circunstancias que parecen venir de "
        "afuera o en personas que funcionan como espejo de lo que internamente "
        "aún no está integrado. El equilibrio entre los dos polos es la clave "
        "para trabajar este tránsito constructivamente."
    ),
}

# ── Modificadores por casa natal del planeta afectado ─────────────────────

HOUSE_MODIFIER: dict[int, str] = {
    1: (
        "Al encontrarse el planeta natal en Casa 1, los efectos de este tránsito "
        "se manifiestan directamente en la identidad, la apariencia personal, "
        "la salud y la forma en que el mundo percibe al nativo. Los cambios "
        "interiores se reflejan en cambios visibles en la imagen o en el cuerpo."
    ),
    2: (
        "Con el planeta natal en Casa 2, el área principal de activación son "
        "los recursos económicos, las posesiones materiales y el sistema de "
        "valores del nativo. Este tránsito puede traer ganancias, pérdidas, "
        "revisión de prioridades o cambios en la relación con el dinero."
    ),
    3: (
        "El planeta natal en Casa 3 dirige los efectos hacia la comunicación, "
        "los estudios, los hermanos, los vecinos y los desplazamientos cortos. "
        "Pueden surgir noticias importantes, cambios en la forma de expresarse "
        "o en las relaciones cotidianas cercanas."
    ),
    4: (
        "Con el planeta natal en Casa 4, los temas se centran en el hogar, "
        "la familia de origen, las raíces emocionales y los bienes raíces. "
        "También puede señalar el final de un ciclo importante de vida, "
        "ya que la Casa 4 representa el 'fin del asunto' en muchos sistemas."
    ),
    5: (
        "El planeta natal en Casa 5 dirige la energía del tránsito hacia "
        "la creatividad, los hijos, el romance, los placeres y la especulación. "
        "Este es un momento que afecta profundamente la capacidad de disfrutar "
        "la vida, expresarse creativamente y relacionarse con lo lúdico."
    ),
    6: (
        "Con el planeta natal en Casa 6, los efectos se centran en la salud "
        "física, los hábitos cotidianos, el trabajo rutinario y las relaciones "
        "de servicio. Es frecuente que este tránsito traiga cambios en la "
        "alimentación, en la rutina laboral o en el estado del cuerpo."
    ),
    7: (
        "El planeta natal en Casa 7 dirige los temas hacia las relaciones "
        "íntimas, la pareja, los socios y los adversarios conocidos. Las "
        "dinámicas de un en uno — ya sea en el amor, en los negocios o en "
        "los conflictos — se ven directamente afectadas por este tránsito."
    ),
    8: (
        "Con el planeta natal en Casa 8, el tránsito toca las capas más "
        "profundas de la psique: herencias, recursos compartidos, sexualidad "
        "profunda, deudas y el miedo a la muerte o a la pérdida. Son momentos "
        "de transformación intensa que pueden involucrar finanzas ajenas o "
        "procesos de duelo y regeneración."
    ),
    9: (
        "El planeta natal en Casa 9 dirige los efectos hacia la filosofía, "
        "la educación superior, los viajes largos, la espiritualidad y las "
        "creencias. Este tránsito puede expandir o cuestionar la visión del "
        "mundo del nativo, impulsando estudios, viajes o búsquedas de sentido."
    ),
    10: (
        "Con el planeta natal en Casa 10, los temas afectan directamente a "
        "la carrera profesional, la reputación pública, la autoridad y los "
        "objetivos a largo plazo. Este es uno de los posicionamientos más "
        "visibles: los cambios son percibidos por el entorno social y laboral."
    ),
    11: (
        "El planeta natal en Casa 11 conecta los efectos con los amigos, "
        "los grupos, las esperanzas y los proyectos colectivos. Este tránsito "
        "puede traer cambios en el círculo social, en la participación "
        "comunitaria o en los ideales y objetivos a futuro."
    ),
    12: (
        "Con el planeta natal en Casa 12, los efectos actúan en el nivel "
        "más oculto e interno: el inconsciente, el aislamiento, los retiros "
        "espirituales, los miedos profundos y los asuntos no resueltos del "
        "pasado. Este tránsito puede traer experiencias de soledad, pero "
        "también de profunda introspección y sanación."
    ),
}

# ── Nota de retrogradación ────────────────────────────────────────────────

RETROGRADE_NOTE = (
    "El planeta en tránsito se encuentra retrógrado en este momento, lo que "
    "modifica significativamente la expresión de su energía: en lugar de "
    "manifestarse hacia afuera con claridad, los temas tienden a procesarse "
    "internamente, revisando situaciones pasadas antes de poder avanzar. "
    "Los efectos pueden sentirse como demoras, replanteos o la reaparición "
    "de asuntos que se creían cerrados. La retrogradación invita a la "
    "reflexión antes que a la acción."
)

# ── Diccionario de interpretaciones base ──────────────────────────────────
# (planeta_transito, planeta_natal) -> texto base
# Prioridad A: Saturno, Urano, Neptuno, Plutón sobre todos los natales
# Prioridad B: Júpiter sobre todos los natales
# Prioridad C: Sol, Luna, Mercurio, Venus, Marte sobre todos los natales
# Prioridad D: Nodo Norte sobre todos los natales

TRANSIT_BASE: dict[tuple[str, str], str] = {

    # ════════════════════════════════════════════════════════════════════════
    # SATURNO EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Saturno", "Sol"): (
        "Saturno en tránsito sobre el Sol natal marca un período de prueba "
        "profunda para la identidad, el ego y el propósito de vida. La "
        "autoridad externa — jefes, instituciones, el tiempo mismo — presiona "
        "sobre la voluntad, exigiendo que el ego madure y se responsabilice "
        "de sus actos. Roles de liderazgo y reconocimiento pueden verse "
        "restringidos temporalmente, no para destruirlos sino para construirlos "
        "sobre bases más sólidas. Si el nativo ha trabajado con honestidad "
        "su propósito, este tránsito consolida logros; si ha evitado "
        "responsabilidades, las traerá al frente con urgencia. Es un momento "
        "de seriedad, no de expansión."
    ),
    ("Saturno", "Luna"): (
        "Saturno sobre la Luna natal es uno de los tránsitos emocionalmente "
        "más exigentes. Las emociones se ven contenidas, reprimidas o puestas "
        "a prueba: el nativo puede sentirse solo, incomprendido, emocionalmente "
        "frío o distante de sus seres queridos. Las relaciones con la madre, "
        "el hogar o la familia de origen pueden atravesar una fase de "
        "reestructuración dolorosa pero necesaria. El cuerpo y los ritmos "
        "cotidianos también pueden verse afectados, con tendencia a la fatiga "
        "o la melancolía. Sin embargo, si se trabaja conscientemente, este "
        "tránsito madura la vida emocional y aporta una solidez afectiva "
        "que antes no existía."
    ),
    ("Saturno", "Mercurio"): (
        "Saturno sobre Mercurio natal concentra y disciplina el pensamiento. "
        "El nativo puede sentir que su mente va más lenta, que le cuesta "
        "comunicarse con fluidez o que sus ideas reciben críticas o no son "
        "bien recibidas. Sin embargo, este tránsito también puede ser "
        "extraordinariamente productivo para estudios profundos, escritura "
        "estructurada o cualquier trabajo que requiera rigor mental. Es "
        "un período ideal para compromisos escritos, contratos y planes "
        "detallados, pero hay que revisar todo cuidadosamente antes de "
        "firmar. El pensamiento superficial da paso a la profundidad."
    ),
    ("Saturno", "Venus"): (
        "Saturno sobre Venus natal pone a prueba las relaciones afectivas "
        "y los valores personales. Las relaciones existentes atraviesan una "
        "fase de seriedad en la que se evalúa si tienen fundamento real o "
        "si solo sobrevivían por comodidad o inercia. Las nuevas relaciones "
        "iniciadas en este período tienden a ser serias, comprometidas y "
        "duraderas, aunque a veces con diferencias de edad. El dinero y "
        "los placeres pueden escasear temporalmente, impulsando una revisión "
        "de hábitos de consumo. El amor se vuelve más austero pero más "
        "verdadero cuando hay base real."
    ),
    ("Saturno", "Marte"): (
        "Saturno sobre Marte natal frena y contiene la energía, la iniciativa "
        "y el deseo de acción. El nativo puede sentir frustración intensa "
        "ante los obstáculos, que parecen multiplicarse justo cuando más "
        "quiere avanzar. La agresividad puede volverse hacia adentro "
        "generando tensión muscular, problemas óseos o desmotivación. "
        "Sin embargo, este tránsito también puede forjar una disciplina "
        "extraordinaria: la energía de Marte, cuando Saturno la canaliza "
        "correctamente, produce trabajo sostenido y resultados duraderos. "
        "La paciencia no es rendición — es estrategia."
    ),
    ("Saturno", "Júpiter"): (
        "Saturno sobre Júpiter natal contrasta la expansión con la contracción. "
        "Los planes ambiciosos que parecían imparables ahora encuentran "
        "límites reales: presupuestos, plazos, regulaciones. El optimismo "
        "excesivo se templa con realismo, y aunque puede sentirse como una "
        "decepción, en realidad es una limpieza que elimina proyectos "
        "inflados sin fundamento. Lo que sobrevive a este tránsito es lo "
        "que realmente vale. Las oportunidades existen, pero requieren "
        "más trabajo y paciencia de lo habitual."
    ),
    ("Saturno", "Saturno"): (
        "El tránsito de Saturno sobre su posición natal es una de las "
        "experiencias astrológicas más significativas del ciclo de vida. "
        "El retorno de Saturno (alrededor de los 29-30 años) marca el fin "
        "de la juventud y el inicio de la madurez adulta; el segundo retorno "
        "(alrededor de los 58-60) inaugura la etapa de la sabiduría. "
        "Es un momento de evaluación profunda: qué estructuras de vida "
        "son auténticas y cuáles se construyeron por miedo u obligación. "
        "Las elecciones hechas aquí tienen consecuencias duraderas que "
        "se extienden décadas. Se requiere honestidad brutal con uno mismo."
    ),
    ("Saturno", "Urano"): (
        "Saturno sobre Urano natal crea tensión entre la necesidad de "
        "libertad y cambio (Urano) y las exigencias de la estructura "
        "y la responsabilidad (Saturno). El nativo puede sentir que sus "
        "impulsos de innovación y rebeldía chocan con las normas, las "
        "instituciones o las circunstancias externas. Este tránsito puede "
        "resultar en una disciplina creativa que canaliza el genio de Urano "
        "en formas concretas y aplicables, o puede manifestarse como "
        "conflictos con autoridades por querer romper moldes sin plan."
    ),
    ("Saturno", "Neptuno"): (
        "Saturno sobre Neptuno natal disuelve ilusiones y enfrenta al "
        "nativo con la realidad concreta. Los sueños, los ideales o las "
        "creencias espirituales que no tenían base sólida se desinflan o "
        "se revelan como autoengaños. Puede haber confusión y desorientación, "
        "especialmente en áreas donde el nativo evitaba ver la verdad. "
        "Sin embargo, es también un tránsito que puede concretar lo "
        "espiritual: proyectos creativos o artísticos que se plasman por "
        "primera vez de forma tangible y disciplinada."
    ),
    ("Saturno", "Plutón"): (
        "Saturno sobre Plutón natal es un tránsito de enorme peso: se unen "
        "el planeta de las estructuras con el planeta de las transformaciones "
        "profundas. Los poderes ocultos, las dinámicas de control y las "
        "estructuras que sostenían el poder del nativo se ven cuestionadas "
        "o reestructuradas. Es frecuente que coincida con fin de ciclos "
        "largos, restructuraciones institucionales o de poder, y con la "
        "necesidad de soltar lo que ya no sirve aunque cueste. "
        "La resistencia prolonga el sufrimiento; la aceptación abre paso "
        "a una forma de poder más auténtica y madura."
    ),
    ("Saturno", "Nodo Norte"): (
        "Saturno sobre el Nodo Norte natal señala un momento de evaluación "
        "kármica: ¿está el nativo avanzando en la dirección que su alma "
        "vino a desarrollar? Las responsabilidades que asume ahora tienen "
        "peso a largo plazo. Este tránsito puede traer la sensación de que "
        "el destino o el deber llaman con urgencia, a veces con tristeza "
        "o peso, pero siempre con una seriedad que no puede ignorarse. "
        "Las decisiones tomadas aquí tienen eco en el karma del alma."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # URANO EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Urano", "Sol"): (
        "Urano sobre el Sol natal es uno de los tránsitos más disruptivos "
        "e inesperados que existen. La identidad, el sentido del yo y la "
        "forma en que el nativo se presenta al mundo pasan por una "
        "revolución interior que puede manifestarse como cambios súbitos "
        "de vida, decisiones radicales inesperadas o liberación de roles "
        "que ya no representan quién es el nativo realmente. El deseo "
        "de libertad e independencia se vuelve irresistible. Lo que no "
        "evolucionó de manera orgánica cambia de forma abrupta. "
        "Es un tránsito de despertar, a veces caótico, pero siempre "
        "con dirección hacia una autenticidad más profunda."
    ),
    ("Urano", "Luna"): (
        "Urano sobre la Luna natal sacude el mundo emocional e instintivo "
        "del nativo. Las rutinas emocionales, los apegos familiares y "
        "los patrones de seguridad que ya eran rígidos se quiebran, "
        "a veces de forma inesperada y perturbadora. El hogar puede cambiar "
        "de ubicación repentinamente; las relaciones familiares pasan por "
        "crisis de liberación. Emocionalmente, hay excitabilidad, necesidad "
        "de espacio y dificultad para sentirse estable. Sin embargo, "
        "este tránsito también libera al nativo de condicionamientos "
        "emocionales ancestrales que impedían el crecimiento."
    ),
    ("Urano", "Mercurio"): (
        "Urano sobre Mercurio natal electrifica la mente: el pensamiento "
        "se vuelve rápido, original, brillante y disruptivo. El nativo "
        "puede recibir insights geniales o cambiar de opinión de forma "
        "repentina, sorprendiendo a quienes lo rodean. La comunicación "
        "se vuelve más impredecible e inconformista. Es un período "
        "excelente para innovación, tecnología, aprendizajes no "
        "convencionales y ideas revolucionarias. El riesgo es la "
        "dispersión mental, la impulsividad en lo que se dice o "
        "la incapacidad de mantener un hilo de pensamiento sostenido."
    ),
    ("Urano", "Venus"): (
        "Urano sobre Venus natal trae cambios inesperados en las "
        "relaciones, los valores y el sentido del placer. Las relaciones "
        "existentes pueden vivir sacudidas que las liberan de dinámicas "
        "asfixiantes o que las rompen si ya no tenían vitalidad real. "
        "Pueden aparecer relaciones nuevas, excitantes y poco "
        "convencionales que llegan de improviso. El gusto estético "
        "puede cambiar radicalmente. Financieramente, puede haber "
        "altibajos inesperados. Es un tránsito que libera pero "
        "que rara vez trae estabilidad afectiva sostenida."
    ),
    ("Urano", "Marte"): (
        "Urano sobre Marte natal libera la energía y la acción de forma "
        "explosiva e impredecible. El nativo siente una urgencia extrema "
        "de actuar, de romper lo que lo contiene y de ir en direcciones "
        "completamente nuevas. Hay riesgo de accidentes por impulsividad "
        "o de conflictos que estallan sin aviso. La sexualidad puede "
        "volverse más experimental y la agresividad más errática. "
        "Si se canaliza bien, este tránsito puede producir iniciativas "
        "valientes y originales que cambian el curso de vida del nativo "
        "de forma permanente."
    ),
    ("Urano", "Júpiter"): (
        "Urano sobre Júpiter natal combina el principio de expansión "
        "con el de cambio súbito. Las oportunidades llegan de formas "
        "inesperadas — viajes repentinos, conocimientos revolucionarios, "
        "cambios de filosofía de vida, conexiones internacionales "
        "imprevistas. La suerte puede aparecer y desaparecer rápidamente. "
        "Las creencias y visión del mundo del nativo se amplían de forma "
        "radical, a veces cuestionando todo lo que creía saber. "
        "Es un período de emocionante incertidumbre y potencial."
    ),
    ("Urano", "Saturno"): (
        "Urano sobre Saturno natal confronta al nativo con la necesidad "
        "de renovar sus estructuras, compromisos y forma de ejercer "
        "la autoridad. Las rutinas y responsabilidades que ya habían "
        "envejecido se ven sacudidas o eliminadas. Puede haber ruptura "
        "con sistemas, instituciones o roles que ya no representan "
        "quién es el nativo. Si el nativo ha construido estructuras "
        "auténticas, este tránsito las libera y moderniza; si construyó "
        "sobre el miedo o la obligación, las derrumba. "
        "La renovación de la autoridad personal está en juego."
    ),
    ("Urano", "Urano"): (
        "El tránsito de Urano sobre su posición natal es uno de los "
        "grandes hitos del ciclo vital. La cuadratura de Urano (alrededor "
        "de los 21 años) coincide con la búsqueda de identidad adulta; "
        "la oposición (alrededor de los 40-42) marca la famosa 'crisis "
        "de la mediana edad'; el segundo trígono (60-63) trae liberación "
        "y la última cuadratura (alrededor de los 63-65) reestructura "
        "la forma de vivir la libertad en la madurez. El retorno de "
        "Urano (alrededor de los 84) es rarísimo. Cada uno de estos "
        "momentos invita a una renovación radical de la identidad."
    ),
    ("Urano", "Neptuno"): (
        "Urano sobre Neptuno natal genera una perturbación en el mundo "
        "de las ilusiones, la espiritualidad y los sueños del nativo. "
        "Las creencias espirituales o artísticas pueden cambiar de forma "
        "abrupta, revelando verdades que antes estaban veladas. "
        "Puede haber despertar espiritual súbito o, por el contrario, "
        "confusión intensa sobre la dirección del alma. Las fantasías "
        "se rompen para dar paso a una espiritualidad más auténtica, "
        "aunque el proceso puede sentirse desorientador."
    ),
    ("Urano", "Plutón"): (
        "Urano sobre Plutón natal es un tránsito de transformación "
        "revolucionaria a nivel muy profundo. Los poderes ocultos, "
        "los procesos de regeneración y las estructuras de control "
        "interno se ven sacudidos por fuerzas que buscan una expresión "
        "completamente nueva. Pueden surgir crisis de poder intensas "
        "o revelaciones perturbadoras sobre dinámicas de dominación. "
        "Este tránsito tiende a producir cambios irreversibles en la "
        "forma en que el nativo ejerce — o cede — su poder personal."
    ),
    ("Urano", "Nodo Norte"): (
        "Urano sobre el Nodo Norte natal sacude el camino evolutivo "
        "del alma de forma abrupta e inesperada. Circunstancias "
        "sorprendentes pueden desviar al nativo de su camino habitual "
        "para llevarlo hacia una dirección kármica que no habría "
        "elegido conscientemente. Este tránsito a veces se siente "
        "como un destino que llega sin pedir permiso, abriendo puertas "
        "que permanecían cerradas o cerrando de golpe las que ya "
        "no debían seguir abiertas."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # NEPTUNO EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Neptuno", "Sol"): (
        "Neptuno sobre el Sol natal es uno de los tránsitos más "
        "disolventes que existen: la identidad, los límites del ego "
        "y el sentido de propósito se vuelven borrosos, permeables "
        "y confusos. El nativo puede sentir que no sabe quién es, "
        "que su energía se dispersa sin dirección o que sus roles "
        "habituales ya no tienen el mismo significado. La fantasía "
        "puede idealizar situaciones o personas, creando ilusiones "
        "que luego se desinflan. Sin embargo, también puede ser un "
        "período de inspiración artística extraordinaria, de apertura "
        "espiritual y de mayor empatía y compasión hacia los demás."
    ),
    ("Neptuno", "Luna"): (
        "Neptuno sobre la Luna natal intensifica la sensibilidad "
        "emocional hasta niveles casi psíquicos. El nativo puede "
        "absorber las emociones de los demás sin filtro, lo que "
        "puede resultar agotador o confuso. Las ilusiones y los "
        "autoengaños en el terreno afectivo son especialmente "
        "frecuentes: es fácil idealizar relaciones o situaciones "
        "y luego desilusionarse cuando la realidad se impone. "
        "Sin embargo, este tránsito también puede traer una "
        "comprensión espiritual profunda de los propios mecanismos "
        "emocionales y una mayor apertura a la intuición."
    ),
    ("Neptuno", "Mercurio"): (
        "Neptuno sobre Mercurio natal nubla el pensamiento racional "
        "y lo tiñe de intuición, fantasía y sensibilidad artística. "
        "El nativo puede tener dificultades para concentrarse, para "
        "comunicarse con claridad o para distinguir la realidad de "
        "la imaginación. Es un período de alta sensibilidad mental "
        "pero de baja fiabilidad lógica: hay que revisar datos, "
        "leer con atención los contratos y no tomar decisiones "
        "importantes basadas en impresiones subjetivas. Por otro lado, "
        "la escritura creativa, la música y el arte pueden florecer "
        "notablemente."
    ),
    ("Neptuno", "Venus"): (
        "Neptuno sobre Venus natal puede traer el amor más idealizado "
        "y romántico que el nativo haya experimentado — pero también "
        "el más ilusorio. Las relaciones iniciadas bajo este tránsito "
        "a menudo tienen un componente de sacrificio, dependencia "
        "o autoengaño que solo se ve claramente cuando el tránsito "
        "termina. También pueden surgir relaciones genuinamente "
        "espirituales y con una calidad de amor incondicional poco "
        "común. Económicamente, hay riesgo de gastos sin control "
        "o de inversiones ilusas."
    ),
    ("Neptuno", "Marte"): (
        "Neptuno sobre Marte natal disuelve la energía, la iniciativa "
        "y la capacidad de acción del nativo. Lo que antes se hacía "
        "con fuerza directa ahora requiere rodeos, paciencia e "
        "incertidumbre. Puede haber falta de motivación, confusión "
        "sobre qué dirección tomar o una energía que se filtra sin "
        "llegar a ningún destino. Sin embargo, las artes marciales, "
        "la danza, la actuación y cualquier forma de acción creativa "
        "o espiritual pueden alcanzar un nivel extraordinario. "
        "El deseo también puede idealizarse o volverse difuso."
    ),
    ("Neptuno", "Júpiter"): (
        "Neptuno sobre Júpiter natal expande los sueños y la "
        "espiritualidad hasta proporciones oceánicas. El idealismo, "
        "la fe y los proyectos visionarios florecen, pero corren el "
        "riesgo de carecer de fundamento práctico. Es un período "
        "de enorme creatividad espiritual y filosófica, pero con "
        "tendencia a prometer más de lo que se puede cumplir "
        "o a creer en proyectos que luego no se materializan. "
        "La distinción entre visión legítima y fantasía es el "
        "desafío central de este tránsito."
    ),
    ("Neptuno", "Saturno"): (
        "Neptuno sobre Saturno natal disuelve lentamente las "
        "estructuras, las responsabilidades y las certezas del nativo. "
        "Lo que antes parecía sólido y predecible se vuelve "
        "inestable, incierto o difícil de mantener. Las estructuras "
        "de vida — trabajo, compromisos, rutinas — pueden desdibujarse "
        "o perder relevancia. Aunque puede sentirse como pérdida de "
        "control, este tránsito tiene el potencial de espiritualizar "
        "el sentido de la responsabilidad y de abrir al nativo a una "
        "forma de estructura más fluida y menos rígida."
    ),
    ("Neptuno", "Urano"): (
        "Neptuno sobre Urano natal mezcla el principio de disolución "
        "con el de despertar. Las revelaciones espirituales pueden "
        "llegar de formas inesperadas, disolviendo la mente racional "
        "para dar paso a una conciencia más amplia. Sin embargo, "
        "también puede haber confusión sobre la dirección del cambio "
        "personal y dificultad para distinguir intuición genuina "
        "de ilusión. Las tecnologías de conciencia — meditación, "
        "estados alterados, arte visionario — pueden ser especialmente "
        "poderosas en este período."
    ),
    ("Neptuno", "Neptuno"): (
        "El tránsito de Neptuno sobre su propia posición natal "
        "(el retorno de Neptuno, alrededor de los 164 años) es "
        "prácticamente imposible en una vida humana. Sin embargo, "
        "la cuadratura de Neptuno (40-42 años) y su oposición "
        "(alrededor de los 82 años) son hitos significativos. "
        "La cuadratura coincide frecuentemente con crisis de "
        "identidad espiritual y con una revisión profunda de los "
        "sueños y las ilusiones de la primera mitad de la vida. "
        "La oposición trae una madurez espiritual única."
    ),
    ("Neptuno", "Plutón"): (
        "Neptuno sobre Plutón natal es un tránsito generacional y "
        "de muy largo plazo que toca los estratos más profundos "
        "de la psique colectiva e individual. Puede traer una "
        "espiritualización de los procesos de transformación y "
        "regeneración del nativo, disolviendo el miedo a las "
        "profundidades. También puede confundir o idealizar los "
        "procesos de poder y control. Este es un tránsito que "
        "trabaja silenciosamente en el inconsciente durante años."
    ),
    ("Neptuno", "Nodo Norte"): (
        "Neptuno sobre el Nodo Norte natal tiñe el camino evolutivo "
        "del alma con idealismo, espiritualidad y confusión. El "
        "nativo puede sentir que su dirección de vida se vuelve "
        "borrosa o que las metas que perseguía ya no le satisfacen "
        "como antes. Es un llamado a elevar la motivación de los "
        "logros materiales hacia una contribución más espiritual "
        "o artística. El riesgo es perderse en fantasías sobre "
        "el destino en lugar de actuar concretamente."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # PLUTÓN EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Plutón", "Sol"): (
        "Plutón sobre el Sol natal es uno de los tránsitos más "
        "transformadores que existen. La identidad, el ego y el "
        "sentido de poder personal pasan por una muerte simbólica "
        "y un renacimiento. Lo que el nativo creía ser — sus roles, "
        "su imagen, sus ambiciones — se deshace para dar paso a "
        "una versión de sí mismo más auténtica y poderosa. El "
        "proceso rara vez es indoloro: puede haber crisis de ego, "
        "confrontaciones con figuras de autoridad o pérdida de "
        "posiciones que el nativo creía seguras. Pero lo que emerge "
        "del otro lado es una voluntad más genuina y menos "
        "dependiente de la validación externa."
    ),
    ("Plutón", "Luna"): (
        "Plutón sobre la Luna natal transforma desde la raíz el "
        "mundo emocional y los vínculos más íntimos del nativo. "
        "Los patrones emocionales heredados, los apegos obsesivos "
        "o los miedos ancestrales salen a la superficie con una "
        "intensidad que puede resultar abrumadora. Relaciones "
        "familiares, especialmente con la madre, pueden pasar por "
        "crisis de transformación profunda. El hogar puede cambiar "
        "radicalmente. Sin embargo, este tránsito también tiene "
        "el poder de sanar heridas emocionales muy antiguas si "
        "el nativo acepta el proceso de transformación."
    ),
    ("Plutón", "Mercurio"): (
        "Plutón sobre Mercurio natal transforma la forma de pensar "
        "y comunicarse del nativo desde sus raíces. El pensamiento "
        "superficial se vuelve insuficiente: hay una compulsión "
        "por investigar a fondo, por descubrir lo que está oculto "
        "y por expresar verdades que antes no podían decirse. "
        "Puede haber obsesión mental, conversaciones intensas "
        "o conflictos comunicativos marcados por el poder y el "
        "control. Los estudios de psicología, investigación, "
        "ciencia oculta y cualquier campo que requiera excavar "
        "bajo la superficie se potencian enormemente."
    ),
    ("Plutón", "Venus"): (
        "Plutón sobre Venus natal transforma radicalmente la vida "
        "afectiva, los valores y la relación con el dinero y el "
        "placer del nativo. Las relaciones existentes atraviesan "
        "un proceso de muerte y renacimiento: las dinámicas de "
        "poder, los celos y la intensidad emocional se agudizan. "
        "Pueden surgir relaciones nuevas marcadas por una atracción "
        "magnética y transformadora que cambia la vida. Los valores "
        "se redefinen desde adentro, eliminando lo que se sostenía "
        "por apariencia y conservando solo lo que es genuino. "
        "Es un tránsito de amor transformador, raramente cómodo."
    ),
    ("Plutón", "Marte"): (
        "Plutón sobre Marte natal intensifica la energía, el deseo "
        "y la capacidad de lucha del nativo hasta niveles extremos. "
        "La voluntad se vuelve poderosa y a veces obsesiva; los "
        "conflictos pueden escalarse de forma inesperada. Hay un "
        "potencial de cambio radical en la forma de actuar en el "
        "mundo — la energía se concentra con un propósito más "
        "profundo que antes. La sexualidad también se transforma, "
        "volviéndose más intensa y compleja. Si se canaliza bien, "
        "este tránsito produce un poder de acción extraordinario; "
        "si no, puede derivar en agresividad o en luchas de poder "
        "que desgastan."
    ),
    ("Plutón", "Júpiter"): (
        "Plutón sobre Júpiter natal amplifica el poder de las "
        "creencias, la filosofía y el potencial de expansión del "
        "nativo, pero también puede volverlo obsesivo o fanático "
        "con sus visiones del mundo. Las oportunidades de crecimiento "
        "son enormes si se trabaja con integridad, especialmente en "
        "áreas de educación, espiritualidad, negocios o influencia "
        "pública. Sin embargo, también puede haber un uso del "
        "conocimiento como herramienta de poder o control. "
        "Es un tránsito de gran potencial para quien está dispuesto "
        "a transformar su filosofía de vida."
    ),
    ("Plutón", "Saturno"): (
        "Plutón sobre Saturno natal destruye y reconstruye las "
        "estructuras fundamentales de la vida del nativo. Las "
        "responsabilidades, los compromisos y los pilares sobre "
        "los que se sostenía la vida pueden derrumbarse o "
        "transformarse radicalmente. Instituciones, cargos de "
        "autoridad o compromisos de largo plazo pueden terminar "
        "o renovarse completamente. El miedo a perder el control "
        "puede ser intenso. Sin embargo, lo que emerge de este "
        "proceso es una estructura de vida más auténtica, basada "
        "en el poder real del nativo y no en el miedo o la inercia."
    ),
    ("Plutón", "Urano"): (
        "Plutón sobre Urano natal genera una transformación "
        "revolucionaria en la forma de ejercer la libertad y "
        "el cambio. Las revoluciones internas pueden volverse "
        "incontrolables, sacudiendo todo lo que el nativo creía "
        "fijo. Puede haber crisis de identidad radical, ruptura "
        "con el pasado de forma definitiva o surgimiento de un "
        "propósito completamente nuevo y más auténtico. Este "
        "tránsito es generacional en su impacto y tiende a "
        "producir cambios irreversibles en la dirección de vida."
    ),
    ("Plutón", "Neptuno"): (
        "Plutón sobre Neptuno natal es un tránsito de transformación "
        "espiritual profunda. Los sueños, las ilusiones y las "
        "creencias espirituales del nativo pasan por un proceso "
        "de muerte y renacimiento que puede manifestarse como "
        "crisis de fe, experiencias de pérdida de ilusiones "
        "o revelaciones espirituales poderosas. Las capas más "
        "profundas del inconsciente se activan, trayendo a la "
        "superficie material que lleva mucho tiempo sumergido "
        "y que necesita ser integrado."
    ),
    ("Plutón", "Plutón"): (
        "El tránsito de Plutón sobre su propia posición natal "
        "es el más lento e infrecuente de todos — el retorno de "
        "Plutón tarda entre 245 y 250 años. Sin embargo, la "
        "cuadratura de Plutón (alrededor de los 35-40 años) "
        "y la oposición (60-70 años) son transformaciones "
        "profundísimas del poder personal y del propósito vital. "
        "La cuadratura confronta al nativo con sus sombras; "
        "la oposición trae una madurez del poder que puede "
        "manifestarse como sabiduría o como crisis de control. "
        "Son hitos de transformación de primera magnitud."
    ),
    ("Plutón", "Nodo Norte"): (
        "Plutón sobre el Nodo Norte natal transforma radicalmente "
        "la dirección evolutiva del alma. El camino de crecimiento "
        "que el nativo creía conocer se ve sacudido por fuerzas "
        "profundas que exigen una renovación total del propósito. "
        "Puede haber una experiencia de muerte simbólica del "
        "'yo que era' para dar paso a una misión más auténtica "
        "y poderosa. Este tránsito a veces coincide con llamadas "
        "vocacionales que ya no pueden ignorarse."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # JÚPITER EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Júpiter", "Sol"): (
        "Júpiter sobre el Sol natal es uno de los tránsitos más "
        "beneficiosos y expansivos del ciclo anual. La confianza "
        "en uno mismo, el optimismo y la vitalidad se disparan; "
        "el nativo siente que puede lograr más, que las puertas "
        "se abren con mayor facilidad y que el reconocimiento "
        "llega de formas naturales. Es un momento ideal para "
        "iniciativas audaces, para pedir aumentos o ascensos y "
        "para comprometerse con proyectos de mayor escala. "
        "El riesgo es el exceso: sobreestimar las fuerzas o "
        "comprometerse más de lo que puede sostenerse."
    ),
    ("Júpiter", "Luna"): (
        "Júpiter sobre la Luna natal expande y alegra la vida "
        "emocional del nativo. Hay mayor facilidad para conectar "
        "con los demás, para sentirse comprendido y para "
        "expresar los sentimientos con generosidad. El hogar "
        "y la familia pueden ampliarse — físicamente a través "
        "de mudanzas o de nuevos miembros, o emocionalmente "
        "a través de mayor apertura y calidez. También es "
        "un período favorable para la alimentación, la salud "
        "y el bienestar cotidiano. Las emociones positivas "
        "fluyen con mayor facilidad."
    ),
    ("Júpiter", "Mercurio"): (
        "Júpiter sobre Mercurio natal expande el pensamiento, "
        "el aprendizaje y las comunicaciones del nativo. "
        "Las ideas fluyen con abundancia y optimismo; los "
        "proyectos de escritura, estudio o enseñanza encuentran "
        "su mejor momento. El pensamiento se vuelve más amplio "
        "y filosófico, interesado en el gran panorama más que "
        "en los detalles. Los contratos, viajes cortos y "
        "negociaciones tienen perspectivas favorables, aunque "
        "hay que cuidar no prometer más de lo que se puede "
        "cumplir por exceso de optimismo."
    ),
    ("Júpiter", "Venus"): (
        "Júpiter sobre Venus natal es el tránsito más bendecido "
        "para el amor, la armonía y la abundancia. Las relaciones "
        "se vuelven más generosas, más alegres y con mayor "
        "apertura mutua. Es un momento excelente para comprometerse, "
        "casarse o iniciar relaciones importantes. También favorece "
        "el dinero, los ingresos y el disfrute de los placeres "
        "de la vida con mayor generosidad. El arte, la belleza "
        "y la creatividad también florecen. "
        "El único riesgo es el exceso en los gastos o en "
        "los compromisos afectivos."
    ),
    ("Júpiter", "Marte"): (
        "Júpiter sobre Marte natal potencia la energía, la acción "
        "y la iniciativa del nativo de forma notable. Hay entusiasmo "
        "desbordante, capacidad de trabajo aumentada y un impulso "
        "de conquistar metas que en otros momentos parecerían "
        "inalcanzables. Es un período ideal para iniciar proyectos "
        "físicamente demandantes, para el deporte y para cualquier "
        "empresa que requiera valentía. El riesgo es la impulsividad "
        "o el exceso: asumir más peleas o proyectos de los que "
        "se pueden manejar."
    ),
    ("Júpiter", "Júpiter"): (
        "El retorno de Júpiter (aproximadamente cada 12 años) "
        "es uno de los ciclos más reconocidos en astrología. "
        "Marca el inicio de un nuevo ciclo de crecimiento "
        "y expansión en todas las áreas de la vida. Los 12 "
        "años previos se sintetizan en sabiduría adquirida, "
        "y el nativo siente un renovado optimismo y apertura "
        "a nuevas posibilidades. Es un momento excelente para "
        "comprometerse con nuevas direcciones y para sembrar "
        "intenciones que darán fruto en el próximo ciclo."
    ),
    ("Júpiter", "Saturno"): (
        "Júpiter sobre Saturno natal alivia temporalmente las "
        "cargas y restricciones que Saturno impone en la vida "
        "del nativo. Las responsabilidades parecen más llevaderas, "
        "el trabajo estructurado recibe reconocimiento y hay "
        "optimismo en áreas donde antes había peso. Es un "
        "período para construir con disciplina y confianza "
        "simultánea: la expansión de Júpiter y la estructura "
        "de Saturno se combinan para crear bases sólidas. "
        "Es uno de los mejores momentos para comprometerse "
        "con proyectos de largo plazo."
    ),
    ("Júpiter", "Urano"): (
        "Júpiter sobre Urano natal abre puertas de forma "
        "inesperada y emocionante. Oportunidades de libertad, "
        "innovación y cambio positivo llegan de formas "
        "sorprendentes. Puede haber un golpe de suerte asociado "
        "a tecnología, inventos, viajes repentinos o decisiones "
        "radicales que dan un giro positivo a la vida. "
        "La expansión de Júpiter amplifica el potencial "
        "revolucionario de Urano: es un momento para atreverse "
        "a hacer lo inusual."
    ),
    ("Júpiter", "Neptuno"): (
        "Júpiter sobre Neptuno natal expande los sueños, la "
        "espiritualidad y la imaginación del nativo hasta "
        "proporciones oceánicas. La fe, la visión artística "
        "y el potencial creativo se potencian enormemente. "
        "Sin embargo, el optimismo puede volverse ilusorio: "
        "proyectos que parecen perfectos pueden carecer de "
        "fundamento práctico, y la tendencia al autoengaño "
        "o a la credulidad puede llevar a decepciones. "
        "Es un período de gran belleza interior que necesita "
        "anclas de realidad."
    ),
    ("Júpiter", "Plutón"): (
        "Júpiter sobre Plutón natal amplifica el poder personal "
        "y la capacidad de transformación del nativo. Las "
        "ambiciones de poder, influencia y cambio se vuelven "
        "más grandes y más alcanzables. Es un período para "
        "liderar transformaciones, para negociar con fuerza "
        "y para acceder a recursos que estaban fuera de alcance. "
        "El potencial de éxito es enorme, pero la tentación de "
        "abusar del poder también se amplifica. "
        "La integridad es la clave para aprovechar este tránsito."
    ),
    ("Júpiter", "Nodo Norte"): (
        "Júpiter sobre el Nodo Norte natal es uno de los tránsitos "
        "más favorables para el crecimiento evolutivo del alma. "
        "Las circunstancias conspiran para ayudar al nativo a "
        "avanzar en su camino de destino, con oportunidades "
        "que parecen llegar como por gracia. Es un momento "
        "de alineación entre el crecimiento personal y el "
        "propósito kármico del alma. No hay que desperdiciar "
        "las puertas que se abren en este período."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # SOL EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Sol", "Sol"): (
        "El tránsito del Sol sobre el Sol natal ocurre una vez "
        "al año y coincide con el cumpleaños solar o retorno solar. "
        "Es un momento de renovación de la identidad, de evaluación "
        "del año transcurrido y de establecimiento de intenciones "
        "para el ciclo que comienza. La vitalidad suele estar "
        "elevada y hay claridad sobre los propósitos personales. "
        "Es el mejor momento del año para tomar decisiones "
        "relacionadas con el propio camino y la expresión personal."
    ),
    ("Sol", "Luna"): (
        "El tránsito del Sol sobre la Luna natal ilumina la vida "
        "emocional y cotidiana del nativo. Los sentimientos se "
        "hacen más visibles — tanto para uno mismo como para "
        "los demás — y las necesidades emocionales piden ser "
        "atendidas. El hogar y la familia cobran protagonismo "
        "durante unos días. Es un momento favorable para "
        "conversaciones emocionales honestas y para conectar "
        "con la propia interioridad con mayor claridad."
    ),
    ("Sol", "Mercurio"): (
        "El tránsito del Sol sobre Mercurio natal ilumina la mente "
        "y la comunicación. El pensamiento se vuelve más claro "
        "y está más expuesto a la voluntad consciente. Es un "
        "buen momento para presentar ideas, firmar documentos, "
        "hacer llamadas importantes o iniciar estudios. "
        "La mente recibe energía y reconocimiento durante "
        "estos días, lo que facilita que las ideas del nativo "
        "sean escuchadas y apreciadas."
    ),
    ("Sol", "Venus"): (
        "El tránsito del Sol sobre Venus natal ilumina el amor, "
        "los valores y el placer del nativo durante unos días. "
        "Es un momento de mayor calidez en las relaciones, de "
        "disfrute de la belleza y de mayor atractivo personal. "
        "Las relaciones afectivas reciben atención positiva y "
        "los valores personales están más claros. Es un buen "
        "momento para actividades sociales, artísticas o "
        "relacionadas con el dinero y los recursos propios."
    ),
    ("Sol", "Marte"): (
        "El tránsito del Sol sobre Marte natal activa y calienta "
        "la energía y el impulso de acción del nativo. Hay "
        "mayor vitalidad, competitividad y disposición para "
        "la acción directa. Es un momento favorable para el "
        "deporte, para confrontaciones directas que se han "
        "postergado o para iniciativas que requieren valentía. "
        "Sin embargo, la impulsividad puede aumentar y hay "
        "que cuidar los conflictos innecesarios."
    ),
    ("Sol", "Júpiter"): (
        "El tránsito del Sol sobre Júpiter natal ilumina y "
        "activa el potencial de expansión y suerte del nativo. "
        "Unos días de mayor optimismo, generosidad y apertura "
        "a nuevas posibilidades. Es un buen momento para "
        "hacer peticiones importantes, para viajes, para "
        "actividades filosóficas o educativas y para mostrar "
        "la mejor versión de uno mismo ante oportunidades "
        "de crecimiento."
    ),
    ("Sol", "Saturno"): (
        "El tránsito del Sol sobre Saturno natal puede traer "
        "unos días de mayor seriedad, responsabilidad y peso. "
        "El nativo puede sentirse más cansado o presionado "
        "por obligaciones, pero también tiene mayor capacidad "
        "de trabajo estructurado y disciplinado. Es un buen "
        "momento para tareas que requieren perseverancia "
        "y concentración, y para evaluar objetivamente "
        "el estado de las responsabilidades actuales."
    ),
    ("Sol", "Urano"): (
        "El tránsito del Sol sobre Urano natal activa "
        "brevemente el potencial de cambio, originalidad "
        "y liberación del nativo. Pueden surgir ideas "
        "brillantes e inesperadas, encuentros inusuales "
        "o impulsos de hacer algo diferente. Es un momento "
        "para la creatividad, la tecnología y las "
        "innovaciones, pero también para estar preparado "
        "ante lo inesperado."
    ),
    ("Sol", "Neptuno"): (
        "El tránsito del Sol sobre Neptuno natal puede traer "
        "unos días de mayor sensibilidad, intuición y "
        "apertura espiritual, pero también de confusión "
        "o falta de claridad en la identidad. El nativo "
        "puede sentirse más poroso e influenciable, lo "
        "que favorece el arte y la empatía pero puede "
        "dificultar la toma de decisiones prácticas. "
        "Es un buen momento para la meditación y el "
        "trabajo creativo."
    ),
    ("Sol", "Plutón"): (
        "El tránsito del Sol sobre Plutón natal activa "
        "brevemente el potencial de poder, transformación "
        "y profundidad del nativo. Pueden surgir conversaciones "
        "o situaciones intensas que revelan verdades ocultas "
        "o dinámicas de poder latentes. Es un momento para "
        "la introspección profunda, para los procesos de "
        "sanación o para hacer valer la propia fuerza "
        "en situaciones que lo requieran."
    ),
    ("Sol", "Nodo Norte"): (
        "El tránsito del Sol sobre el Nodo Norte natal ilumina "
        "brevemente el camino evolutivo del alma del nativo. "
        "Puede haber claridad momentánea sobre la dirección "
        "correcta, encuentros significativos desde el punto "
        "de vista del destino o situaciones que le recuerdan "
        "al nativo dónde debe enfocar su energía para crecer."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # LUNA EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Luna", "Sol"): (
        "El tránsito de la Luna sobre el Sol natal activa las "
        "emociones en relación con la identidad y el propósito "
        "del nativo durante unas horas o un día. Hay mayor "
        "sensibilidad a cómo se es percibido y una necesidad "
        "instintiva de reconocimiento emocional. Es un momento "
        "para escuchar las propias necesidades afectivas en "
        "relación con los roles que se desempeñan."
    ),
    ("Luna", "Luna"): (
        "El tránsito de la Luna sobre su posición natal ocurre "
        "aproximadamente cada 28 días y marca un reinicio del "
        "ciclo emocional mensual. Las emociones y necesidades "
        "instintivas están especialmente activas, y hay mayor "
        "receptividad emocional y necesidad de conexión "
        "con el hogar y la familia. Es un momento de "
        "evaluación breve pero intensa del estado emocional."
    ),
    ("Luna", "Mercurio"): (
        "El tránsito de la Luna sobre Mercurio natal mezcla "
        "las emociones con el pensamiento durante unas horas. "
        "Las conversaciones pueden volverse más emocionales "
        "o intuitivas; las decisiones tienden a ser influidas "
        "por el estado de ánimo más que por la lógica pura. "
        "Es un buen momento para la escritura creativa o "
        "para conversaciones que requieren sensibilidad."
    ),
    ("Luna", "Venus"): (
        "El tránsito de la Luna sobre Venus natal activa la "
        "necesidad de amor, conexión y belleza durante unas "
        "horas. El nativo puede sentir mayor apetito por "
        "la compañía, el afecto y los placeres sensoriales. "
        "Las relaciones afectivas tienen un tono más suave "
        "y receptivo, y es un momento favorable para la "
        "sociabilidad y las actividades artísticas."
    ),
    ("Luna", "Marte"): (
        "El tránsito de la Luna sobre Marte natal puede traer "
        "irritabilidad emocional, reacciones impulsivas o "
        "mayor energía física durante unas horas. Las emociones "
        "se expresan con más directidad y calor, lo que puede "
        "derivar en conflictos si no se gestiona con conciencia. "
        "Sin embargo, también hay mayor coraje para expresar "
        "lo que se siente sin rodeos."
    ),
    ("Luna", "Júpiter"): (
        "El tránsito de la Luna sobre Júpiter natal trae "
        "unas horas de buen humor, generosidad emocional "
        "y apertura. El nativo puede sentirse optimista, "
        "sociable y con ganas de compartir con los demás. "
        "Las emociones se expanden y hay facilidad para "
        "ver el lado positivo de las situaciones. "
        "Un pequeño pero agradable impulso de bienestar."
    ),
    ("Luna", "Saturno"): (
        "El tránsito de la Luna sobre Saturno natal puede "
        "traer unas horas de melancolía, seriedad emocional "
        "o sensación de soledad. El nativo puede sentirse "
        "más distante, reprimido en sus emociones o presionado "
        "por las responsabilidades. Es una señal para cuidar "
        "el estado emocional, descansar y no tomar decisiones "
        "importantes desde la tristeza o el agotamiento."
    ),
    ("Luna", "Urano"): (
        "El tránsito de la Luna sobre Urano natal puede traer "
        "unas horas de excitación emocional, imprevisibilidad "
        "o nerviosismo. Las emociones pueden cambiar de forma "
        "repentina y el nativo puede sentirse inquieto o con "
        "ganas de romper la rutina. Es un momento para la "
        "espontaneidad, pero hay que cuidar las reacciones "
        "impulsivas."
    ),
    ("Luna", "Neptuno"): (
        "El tránsito de la Luna sobre Neptuno natal intensifica "
        "la sensibilidad psíquica y emocional durante unas "
        "horas. Los sueños pueden ser especialmente vívidos, "
        "la intuición se agudiza y hay mayor permeabilidad "
        "a las emociones ajenas. Es un momento favorable "
        "para la meditación, el arte y la empatía, pero "
        "también para el autoengaño emocional."
    ),
    ("Luna", "Plutón"): (
        "El tránsito de la Luna sobre Plutón natal puede traer "
        "unas horas de emociones intensas, oscuras o "
        "transformadoras. Pueden surgir celos, obsesiones "
        "emocionales breves o la necesidad de profundizar "
        "en algo. El inconsciente puede enviar señales "
        "claras que vale la pena atender. Es un momento "
        "de intensidad que puede usarse para la introspección."
    ),
    ("Luna", "Nodo Norte"): (
        "El tránsito de la Luna sobre el Nodo Norte natal "
        "activa brevemente la dirección evolutiva del alma. "
        "El nativo puede sentir instintivamente que está "
        "en el lugar correcto o que algo le llama hacia "
        "su camino de crecimiento. Es un momento para "
        "prestar atención a las señales intuitivas."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # MERCURIO EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Mercurio", "Sol"): (
        "El tránsito de Mercurio sobre el Sol natal activa la "
        "mente y la comunicación en relación con la identidad "
        "del nativo. Es un buen momento para pensar sobre "
        "los propios objetivos, para comunicar quién se es "
        "y para recibir información relevante para el propio "
        "camino. Las ideas fluyen con mayor claridad en "
        "relación con el propósito personal."
    ),
    ("Mercurio", "Luna"): (
        "El tránsito de Mercurio sobre la Luna natal facilita "
        "la expresión de las emociones a través de las palabras. "
        "El nativo puede hablar con mayor facilidad sobre "
        "sus sentimientos o recibir noticias relacionadas "
        "con el hogar y la familia. Es un buen momento "
        "para conversaciones emocionales que requieren "
        "articulación y claridad."
    ),
    ("Mercurio", "Mercurio"): (
        "El tránsito de Mercurio sobre su posición natal "
        "activa la mente del nativo con mayor agudeza. "
        "El pensamiento está especialmente ágil, las "
        "comunicaciones fluyen bien y hay facilidad para "
        "el aprendizaje y el intercambio de ideas. "
        "Es un momento favorable para estudiar, escribir, "
        "negociar o iniciar conversaciones importantes."
    ),
    ("Mercurio", "Venus"): (
        "El tránsito de Mercurio sobre Venus natal facilita "
        "las conversaciones sobre el amor, el dinero y los "
        "valores. El nativo puede recibir propuestas afectivas, "
        "hablar con sus seres queridos con mayor facilidad "
        "o encontrar las palabras para expresar lo que "
        "aprecia. Es un momento favorable para negociaciones "
        "financieras o artísticas."
    ),
    ("Mercurio", "Marte"): (
        "El tránsito de Mercurio sobre Marte natal carga la "
        "comunicación con energía y a veces con combatividad. "
        "El nativo puede hablar con mayor directidad, urgencia "
        "o decisión. Las conversaciones pueden volverse "
        "debates o confrontaciones si no se cuida el tono. "
        "Sin embargo, también es un buen momento para "
        "defender posiciones o para negociaciones que "
        "requieren firmeza."
    ),
    ("Mercurio", "Júpiter"): (
        "El tránsito de Mercurio sobre Júpiter natal expande "
        "el pensamiento hacia horizontes más amplios. "
        "Las ideas son optimistas y generosas, con tendencia "
        "a ver el gran panorama por encima de los detalles. "
        "Es un momento favorable para aprender, planificar "
        "o hacer promesas, aunque hay que cuidar no "
        "exagerar las expectativas comunicativas."
    ),
    ("Mercurio", "Saturno"): (
        "El tránsito de Mercurio sobre Saturno natal puede "
        "traer seriedad mental, pensamiento detallado "
        "y comunicación más formal. Las conversaciones "
        "importantes o la firma de documentos tienen "
        "mayor peso ahora. Es un buen momento para "
        "planificación rigurosa pero no para improvisación "
        "comunicativa."
    ),
    ("Mercurio", "Urano"): (
        "El tránsito de Mercurio sobre Urano natal electrifica "
        "brevemente el pensamiento. Pueden surgir ideas "
        "brillantes e inesperadas, conversaciones estimulantes "
        "sobre temas innovadores o noticias sorprendentes. "
        "El nativo puede hablar más rápido de lo habitual "
        "y saltar de tema con facilidad."
    ),
    ("Mercurio", "Neptuno"): (
        "El tránsito de Mercurio sobre Neptuno natal puede "
        "nublar brevemente el pensamiento racional con "
        "mayor intuición y sensibilidad. La comunicación "
        "puede ser más poética o ambigua. Es un buen "
        "momento para la escritura creativa, pero hay "
        "que revisar con cuidado cualquier contrato "
        "o compromiso verbal."
    ),
    ("Mercurio", "Plutón"): (
        "El tránsito de Mercurio sobre Plutón natal activa "
        "el pensamiento investigativo y profundo. Las "
        "conversaciones pueden volverse intensas o reveladoras, "
        "sacando a la luz información que estaba oculta. "
        "Es un buen momento para investigar, para la "
        "psicología o para cualquier diálogo que requiera "
        "ir al fondo de las cosas."
    ),
    ("Mercurio", "Nodo Norte"): (
        "El tránsito de Mercurio sobre el Nodo Norte natal "
        "puede traer información, conversaciones o encuentros "
        "que resultan significativos para el camino evolutivo "
        "del nativo. Vale la pena prestar atención a los "
        "mensajes y datos que llegan durante este período."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # VENUS EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Venus", "Sol"): (
        "El tránsito de Venus sobre el Sol natal aporta "
        "calidez, gracia y encanto a la expresión personal "
        "del nativo durante unos días. El atractivo personal "
        "se refuerza y hay mayor facilidad para conectar "
        "con los demás. Es un momento favorable para "
        "el amor, las actividades sociales y la presentación "
        "de uno mismo en contextos públicos."
    ),
    ("Venus", "Luna"): (
        "El tránsito de Venus sobre la Luna natal armoniza "
        "el mundo emocional y las relaciones cotidianas. "
        "El nativo se siente más amado y con mayor capacidad "
        "de dar afecto. Las relaciones familiares y del "
        "hogar tienen un tono más suave y armonioso. "
        "Es un buen momento para actividades que combinan "
        "el cuidado emocional con el placer."
    ),
    ("Venus", "Mercurio"): (
        "El tránsito de Venus sobre Mercurio natal hace "
        "que el habla sea más dulce, persuasiva y agradable. "
        "Las conversaciones afectivas fluyen con facilidad "
        "y el nativo puede encontrar las palabras justas "
        "para decir lo que siente. Es un buen momento "
        "para cartas de amor, propuestas o negociaciones "
        "que requieren tacto y diplomacia."
    ),
    ("Venus", "Venus"): (
        "El retorno de Venus sobre su posición natal "
        "marca un reinicio del ciclo afectivo personal. "
        "Los valores, el amor propio y las relaciones "
        "se actualizan. Es un momento especialmente "
        "favorable para el amor, la armonía y los placeres "
        "de la vida, con mayor facilidad para atraer "
        "lo que se valora y desea."
    ),
    ("Venus", "Marte"): (
        "El tránsito de Venus sobre Marte natal mezcla "
        "el amor con el deseo de forma intensa y vivaz. "
        "La sexualidad se activa, el encanto magnético "
        "aumenta y las relaciones pueden tener una "
        "corriente de pasión y atracción notable. "
        "También puede haber tensión en las relaciones "
        "si los valores y los impulsos chocan."
    ),
    ("Venus", "Júpiter"): (
        "El tránsito de Venus sobre Júpiter natal es "
        "especialmente favorable para el amor y la "
        "abundancia. La generosidad, el buen humor y "
        "el disfrute de los placeres alcanzan su punto "
        "más alto. Hay una sensación de que la vida "
        "es abundante y vale la pena disfrutarla. "
        "Las relaciones afectivas y económicas tienen "
        "perspectivas especialmente positivas."
    ),
    ("Venus", "Saturno"): (
        "El tránsito de Venus sobre Saturno natal puede "
        "traer unos días de amor más serio o más austero. "
        "Las relaciones piden compromiso y hay mayor "
        "evaluación de qué relaciones tienen base real. "
        "No es el momento más liviano para el romance, "
        "pero sí para comprometerse con relaciones "
        "que tienen estructura y profundidad."
    ),
    ("Venus", "Urano"): (
        "El tránsito de Venus sobre Urano natal puede "
        "traer encuentros afectivos inesperados o un "
        "deseo repentino de libertad y novedad en las "
        "relaciones. Las personas que se conocen ahora "
        "pueden llegar de formas sorprendentes. "
        "El aburrimiento en las relaciones existentes "
        "se hace más evidente."
    ),
    ("Venus", "Neptuno"): (
        "El tránsito de Venus sobre Neptuno natal puede "
        "traer unos días de romanticismo intenso, "
        "sensibilidad artística elevada o idealización "
        "en las relaciones. La belleza y la espiritualidad "
        "se unen de forma poética. Sin embargo, el "
        "autoengaño en el amor es posible — mejor "
        "disfrutar la sensibilidad sin tomar decisiones "
        "definitivas."
    ),
    ("Venus", "Plutón"): (
        "El tránsito de Venus sobre Plutón natal activa "
        "brevemente una corriente de atracción intensa "
        "y transformadora en las relaciones. Pueden "
        "surgir encuentros magnéticos o dinámicas "
        "de poder en las relaciones afectivas. "
        "Es un momento de pasión pero también de mayor "
        "intensidad emocional en los vínculos."
    ),
    ("Venus", "Nodo Norte"): (
        "El tránsito de Venus sobre el Nodo Norte natal "
        "puede traer relaciones o encuentros afectivos "
        "que tienen una resonancia kármica o una "
        "importancia especial para el crecimiento "
        "del alma del nativo."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # MARTE EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Marte", "Sol"): (
        "El tránsito de Marte sobre el Sol natal activa "
        "la energía, la voluntad y la capacidad de lucha "
        "del nativo de forma notable. Hay mayor vitalidad, "
        "competitividad y disposición para tomar la "
        "iniciativa. Es un buen momento para proyectos "
        "que requieren esfuerzo físico o valentía, pero "
        "la impulsividad puede generar conflictos si "
        "no se gestiona con conciencia."
    ),
    ("Marte", "Luna"): (
        "El tránsito de Marte sobre la Luna natal puede "
        "traer irritabilidad emocional, reacciones más "
        "directas y urgentes, o una mayor energía en "
        "el ámbito doméstico. Las emociones se expresan "
        "con más calor y a veces con agresividad. "
        "Es importante cuidar los conflictos familiares "
        "y gestionar la frustración emocional con "
        "mayor conciencia."
    ),
    ("Marte", "Mercurio"): (
        "El tránsito de Marte sobre Mercurio natal carga "
        "la comunicación con energía y urgencia. El nativo "
        "puede hablar con mayor directidad y decisión, "
        "pero también con más brusquedad. Es un momento "
        "favorable para debates, negociaciones firmes "
        "o cualquier actividad mental que requiera "
        "agresividad intelectual controlada."
    ),
    ("Marte", "Venus"): (
        "El tránsito de Marte sobre Venus natal activa "
        "la pasión, el deseo y la energía en las relaciones "
        "afectivas. La atracción magnética aumenta y "
        "hay mayor iniciativa en el amor y en la búsqueda "
        "de placer. Sin embargo, los conflictos en las "
        "relaciones también pueden avivarse si hay "
        "tensiones no resueltas."
    ),
    ("Marte", "Marte"): (
        "El retorno de Marte sobre su posición natal "
        "(aproximadamente cada dos años) marca un reinicio "
        "del ciclo de iniciativas y deseos del nativo. "
        "La energía, la motivación y la capacidad de "
        "acción se renuevan. Es un momento para relanzar "
        "proyectos, retomar la actividad física y "
        "establecer nuevas metas de acción."
    ),
    ("Marte", "Júpiter"): (
        "El tránsito de Marte sobre Júpiter natal amplifica "
        "la energía y el entusiasmo de forma considerable. "
        "Hay valentía, optimismo y una sensación de que "
        "las acciones tienen mayor alcance y posibilidades "
        "de éxito. Es un excelente momento para iniciativas "
        "audaces, pero hay que cuidar el exceso de "
        "confianza o la sobreextensión."
    ),
    ("Marte", "Saturno"): (
        "El tránsito de Marte sobre Saturno natal puede "
        "generar una energía contenida, frustrada o "
        "muy disciplinada. El impulso de acción choca "
        "con la necesidad de estructura y responsabilidad. "
        "Es un momento de trabajo duro y sostenido si "
        "se canaliza bien, o de frustración y bloqueo "
        "si el nativo trata de forzar resultados sin "
        "la preparación adecuada."
    ),
    ("Marte", "Urano"): (
        "El tránsito de Marte sobre Urano natal combina "
        "el impulso de acción con el de cambio radical. "
        "Pueden surgir iniciativas valientes e inesperadas "
        "o reacciones impulsivas ante situaciones que "
        "se perciben como restrictivas. Hay riesgo de "
        "accidentes por impulsividad. Sin embargo, "
        "este es también un momento de potencial "
        "innovador y de coraje para lo inusual."
    ),
    ("Marte", "Neptuno"): (
        "El tránsito de Marte sobre Neptuno natal puede "
        "confundir el impulso de acción: el nativo puede "
        "sentir que su energía se dispersa sin dirección "
        "clara o que sus motivaciones son confusas. "
        "Es un momento favorable para las artes de "
        "acción — danza, artes marciales, actuación — "
        "pero no para confrontaciones directas o "
        "decisiones de alto riesgo."
    ),
    ("Marte", "Plutón"): (
        "El tránsito de Marte sobre Plutón natal activa "
        "el poder y la intensidad del nativo de forma "
        "notable. La energía se concentra con una "
        "fuerza poderosa que puede manifestarse como "
        "grandes logros o como conflictos de poder "
        "intensos. La sexualidad también se activa. "
        "Es un momento para acciones transformadoras "
        "pero hay que evitar la agresividad o la "
        "manipulación."
    ),
    ("Marte", "Nodo Norte"): (
        "El tránsito de Marte sobre el Nodo Norte natal "
        "activa el impulso de avanzar en el camino "
        "evolutivo del alma. El nativo puede sentir "
        "una urgencia o deseo de actuar en la dirección "
        "de su destino. Es un momento para iniciativas "
        "que se alineen con el propósito más profundo "
        "del alma."
    ),

    # ════════════════════════════════════════════════════════════════════════
    # NODO NORTE EN TRÁNSITO
    # ════════════════════════════════════════════════════════════════════════

    ("Nodo Norte", "Sol"): (
        "El tránsito del Nodo Norte sobre el Sol natal "
        "activa la dirección kármica del alma en relación "
        "con la identidad y el propósito de vida. El nativo "
        "puede sentir un llamado evolutivo claro: circunstancias "
        "que lo empujan hacia una expresión más auténtica "
        "de quién es. Encuentros significativos para el "
        "crecimiento del alma pueden llegar en este período."
    ),
    ("Nodo Norte", "Luna"): (
        "El tránsito del Nodo Norte sobre la Luna natal "
        "activa el camino evolutivo en el terreno emocional "
        "y los vínculos del hogar. El alma está siendo "
        "llamada a sanar y evolucionar en su vida afectiva "
        "familiar. Es un período para trabajar patrones "
        "emocionales ancestrales con vistas al crecimiento."
    ),
    ("Nodo Norte", "Mercurio"): (
        "El tránsito del Nodo Norte sobre Mercurio natal "
        "activa el aprendizaje y la comunicación en el "
        "contexto del destino del alma. El nativo puede "
        "recibir información clave, encontrarse con "
        "maestros o hacer contactos que resulten "
        "importantes para su camino evolutivo."
    ),
    ("Nodo Norte", "Venus"): (
        "El tránsito del Nodo Norte sobre Venus natal "
        "señala que el alma del nativo está siendo "
        "llamada a evolucionar a través del amor y "
        "las relaciones. Encuentros afectivos con "
        "resonancia kármica pueden surgir, o las "
        "relaciones existentes adquieren un significado "
        "más profundo y evolutivo."
    ),
    ("Nodo Norte", "Marte"): (
        "El tránsito del Nodo Norte sobre Marte natal "
        "activa el camino evolutivo a través de la acción "
        "y el coraje. El alma está aprendiendo a actuar "
        "con mayor valentía en la dirección de su destino. "
        "Pueden surgir situaciones que requieren iniciativa "
        "y que son importantes para el crecimiento del alma."
    ),
    ("Nodo Norte", "Júpiter"): (
        "El tránsito del Nodo Norte sobre Júpiter natal "
        "amplifica las oportunidades kármicas de crecimiento "
        "y expansión. El alma está siendo llamada a "
        "expandirse en la dirección de su propósito. "
        "Las oportunidades de crecimiento filosófico, "
        "educativo o espiritual tienen especial relevancia."
    ),
    ("Nodo Norte", "Saturno"): (
        "El tránsito del Nodo Norte sobre Saturno natal "
        "activa el camino evolutivo en el terreno de las "
        "responsabilidades y la madurez. El alma está "
        "aprendiendo a construir con disciplina en la "
        "dirección de su destino. Las estructuras de vida "
        "que se construyen ahora tienen una importancia "
        "kármica especial."
    ),
    ("Nodo Norte", "Urano"): (
        "El tránsito del Nodo Norte sobre Urano natal "
        "señala un llamado evolutivo hacia la innovación "
        "y la liberación de patrones obsoletos. El alma "
        "está siendo invitada a abrazar su originalidad "
        "y a contribuir con sus dones únicos al colectivo."
    ),
    ("Nodo Norte", "Neptuno"): (
        "El tránsito del Nodo Norte sobre Neptuno natal "
        "activa el camino evolutivo en el terreno "
        "espiritual y artístico. El alma está siendo "
        "llamada hacia una expresión más elevada de "
        "su sensibilidad y su conexión con lo trascendente."
    ),
    ("Nodo Norte", "Plutón"): (
        "El tránsito del Nodo Norte sobre Plutón natal "
        "activa el camino evolutivo en el terreno del "
        "poder y la transformación. El alma está siendo "
        "llamada a transformar profundamente su relación "
        "con el poder personal, soltando lo que ya "
        "no sirve para abrazar una forma más auténtica "
        "de influencia."
    ),
    ("Nodo Norte", "Nodo Norte"): (
        "El tránsito del Nodo Norte sobre su posición natal "
        "(el retorno del Nodo Norte, cada 18 años "
        "aproximadamente) marca un momento de renovación "
        "kármica importante. El alma evalúa el camino "
        "recorrido en los últimos 18 años y recibe "
        "un nuevo impulso en la dirección de su destino "
        "evolutivo. Es un momento de compromiso renovado "
        "con el propósito del alma."
    ),
}


# ── Función de construcción de interpretación ─────────────────────────────

def _generic_base(transit_planet: str, natal_planet: str) -> str:
    """Interpretación genérica cuando no hay entrada específica en TRANSIT_BASE."""
    t_theme = _PLANET_THEMES.get(transit_planet, transit_planet)
    n_theme = _PLANET_THEMES.get(natal_planet, natal_planet)
    return (
        f"El tránsito de {transit_planet} activa el área natal de {natal_planet}. "
        f"{transit_planet} rige temas de {t_theme}. "
        f"{natal_planet} natal representa {n_theme} en la carta del nativo. "
        f"Esta combinación pone en juego ambas esferas durante el período del tránsito, "
        f"invitando al nativo a integrar conscientemente las energías implicadas."
    )


def build_transit_interpretation(
    transit_planet: str,
    natal_planet: str,
    aspect_name: str,
    natal_house: int,
    transit_retrograde: bool,
) -> str:
    """
    Ensambla la interpretación completa de un aspecto de tránsito.

    Args:
        transit_planet: nombre del planeta en tránsito
        natal_planet:   nombre del planeta natal afectado
        aspect_name:    tipo de aspecto (Conjunción, Trígono, etc.)
        natal_house:    casa natal donde está el planeta natal
        transit_retrograde: si el planeta en tránsito es retrógrado

    Returns:
        Texto de interpretación completo, con secciones separadas por doble salto.
    """
    key = (transit_planet, natal_planet)
    base = TRANSIT_BASE.get(key) or _generic_base(transit_planet, natal_planet)
    asp_mod = ASPECT_MODIFIER.get(aspect_name, "")
    house_mod = HOUSE_MODIFIER.get(natal_house, "")
    retro = RETROGRADE_NOTE if transit_retrograde else ""

    parts = [p for p in [base, asp_mod, house_mod, retro] if p]
    return "\n\n".join(parts)
