"""Interpretaciones detalladas para carta natal.

Estructura:
- PLANET_IN_SIGN[(planeta, signo)]  -> texto 3-4 frases
- PLANET_IN_HOUSE[(planeta, casa)]  -> texto 2-3 frases
- NOTABLE_ASPECTS[(p1, aspecto, p2)] -> texto específico del par
- ASC_IN_SIGN[signo]                -> interpretación del Ascendente
- build_natal_planet_text()         -> ensambla texto completo por planeta
"""

from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────
# ASCENDENTE POR SIGNO
# ─────────────────────────────────────────────────────────────────────────────

ASC_IN_SIGN: dict[str, str] = {
    "Aries": (
        "El Ascendente en Aries proyecta una imagen directa, enérgica y pionera. "
        "Te presentas ante el mundo con confianza e iniciativa, y los demás te perciben "
        "como alguien de acción, impaciente y con liderazgo natural. "
        "Tu físico tiende a ser atlético o de movimientos rápidos; das la impresión de "
        "estar siempre a punto de dar el siguiente paso. El regente de tu carta es Marte."
    ),
    "Tauro": (
        "El Ascendente en Tauro proyecta solidez, calma y confiabilidad. "
        "Los demás te perciben como alguien calmado, sensual y de fiar; tardas en "
        "reaccionar, pero cuando lo haces tu determinación es inamovible. "
        "Tu físico suele ser robusto o de apariencia cuidada, con atención al estilo. "
        "El regente de tu carta es Venus."
    ),
    "Géminis": (
        "El Ascendente en Géminis proyecta curiosidad, versatilidad y elocuencia. "
        "Los demás te ven como alguien comunicativo, ágil mentalmente y lleno de ideas; "
        "puedes parecer nervioso o disperso cuando el entorno es muy lento para ti. "
        "Tu físico tiende a ser delgado y juvenil, con gestos expresivos. "
        "El regente de tu carta es Mercurio."
    ),
    "Cáncer": (
        "El Ascendente en Cáncer proyecta sensibilidad, calidez y una presencia que "
        "invita a la confianza emocional. Los demás te perciben como empático, protector "
        "y con una fuerte conexión con la familia y el pasado. "
        "Tu apariencia puede cambiar notablemente según tu estado interior. "
        "El regente de tu carta es la Luna."
    ),
    "Leo": (
        "El Ascendente en Leo proyecta carisma, generosidad y presencia escénica natural. "
        "Los demás te ven como alguien cálido, orgulloso y que ocupa el espacio con "
        "dignidad; inspiras respeto y admiración sin apenas proponértelo. "
        "Tu apariencia tiende a ser distinguida, con cabello abundante o un porte señorial. "
        "El regente de tu carta es el Sol."
    ),
    "Virgo": (
        "El Ascendente en Virgo proyecta precisión, discreción y una observación aguda "
        "del entorno. Los demás te perciben como analítico, servicial y meticuloso; "
        "a veces puedes parecer reservado o crítico antes de conocerte bien. "
        "Tu apariencia suele ser limpia, ordenada y con atención al detalle. "
        "El regente de tu carta es Mercurio."
    ),
    "Libra": (
        "El Ascendente en Libra proyecta elegancia, diplomacia y una búsqueda instintiva "
        "de equilibrio. Los demás te ven como encantador, educado y amante de la armonía; "
        "puedes parecer indeciso porque siempre ves ambas partes de la balanza. "
        "Tu apariencia tiende a ser atractiva y bien proporcionada. "
        "El regente de tu carta es Venus."
    ),
    "Escorpio": (
        "El Ascendente en Escorpio proyecta intensidad, magnetismo y una profundidad "
        "que los demás sienten aunque no sepan explicar. Te perciben como reservado, "
        "penetrante y con una voluntad de hierro; tu mirada suele ser especialmente "
        "expresiva. Tus motivaciones reales raramente están a la vista. "
        "El regente de tu carta es Marte (y Plutón como co-regente moderno)."
    ),
    "Sagitario": (
        "El Ascendente en Sagitario proyecta optimismo, franqueza y un espíritu "
        "aventurero que contagia entusiasmo. Los demás te ven como jovial, filosófico "
        "y siempre con un horizonte por conquistar; tu honestidad puede rozar la "
        "imprudencia a veces. Tu físico suele ser alto o de movimientos amplios y expansivos. "
        "El regente de tu carta es Júpiter."
    ),
    "Capricornio": (
        "El Ascendente en Capricornio proyecta seriedad, ambición y una madurez que "
        "a veces aparece desde la infancia. Los demás te perciben como responsable, "
        "contenido y digno de confianza para las tareas importantes; con la edad, "
        "paradójicamente, te vas haciendo más ligero y jovial. "
        "El regente de tu carta es Saturno."
    ),
    "Acuario": (
        "El Ascendente en Acuario proyecta originalidad, independencia y una visión "
        "del mundo que suele adelantarse a su tiempo. Los demás te ven como intelectual, "
        "algo excéntrico y difícil de encasillar; valoras profundamente tu libertad "
        "y rechazas las etiquetas. Tu apariencia suele ser singular o poco convencional. "
        "El regente de tu carta es Saturno (y Urano como co-regente moderno)."
    ),
    "Piscis": (
        "El Ascendente en Piscis proyecta suavidad, empatía y un aura casi etérea que "
        "hace que los demás te vean como compasivo, artístico e intuitivo. "
        "Absorbes el ambiente emocional de tu entorno como una esponja; necesitas "
        "proteger tu energía conscientemente. Tu apariencia puede ser cambiante, "
        "con ojos muy expresivos. El regente de tu carta es Júpiter (y Neptuno moderno)."
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
# PLANETA EN SIGNO
# ─────────────────────────────────────────────────────────────────────────────

PLANET_IN_SIGN: dict[tuple[str, str], str] = {

    # ── SOL ──────────────────────────────────────────────────────────────────
    ("Sol", "Aries"): (
        "Tu identidad es pionera, directa y apasionada por los comienzos. "
        "Brillas cuando lideras, compites o te lanzas a territorios inexplorados; "
        "el fuego de Aries alimenta tu ego con un impulso constante hacia la acción. "
        "El desafío es aprender a sostener los proyectos una vez superado el entusiasmo inicial "
        "y gestionar la impaciencia cuando los resultados no llegan de inmediato."
    ),
    ("Sol", "Tauro"): (
        "Tu identidad es sólida, sensorial y centrada en la creación de seguridad material y emocional. "
        "Brillas a través de la constancia, el buen gusto y la capacidad de sostener lo que has construido. "
        "Tus talentos florecen mejor en entornos estables donde puedas avanzar a tu ritmo. "
        "El desafío es la resistencia al cambio: a veces el apego a lo conocido limita tu crecimiento."
    ),
    ("Sol", "Géminis"): (
        "Tu identidad es curiosa, adaptable y multidimensional; te nutres del intercambio de ideas y "
        "de la variedad. Brillas cuando comunicas, aprendes o conectas a personas e ideas distintas. "
        "Tu mente ágil te convierte en excelente divulgador, escritor o interlocutor. "
        "El desafío es la dispersión: sin foco, la versatilidad puede volverse superficialidad."
    ),
    ("Sol", "Cáncer"): (
        "Tu identidad está íntimamente ligada a la familia, el hogar y el mundo emocional. "
        "Brillas cuando cuidas, proteges y creas un espacio de pertenencia para quienes amas. "
        "Tu intuición es una de tus mayores fortalezas; sientes el estado emocional de las "
        "situaciones antes de analizarlo. El desafío es separar tu bienestar del estado anímico "
        "de los demás y gestionar el miedo al abandono."
    ),
    ("Sol", "Leo"): (
        "Tu identidad es luminosa, generosa y necesita expresarse creativamente. "
        "Brillas cuando eres el centro de atención, cuando lideras con el corazón y cuando "
        "ayudas a otros a brillar también. El reconocimiento y la admiración son combustible "
        "genuino para ti, no vanidad superficial. El desafío es aprender que el amor propio "
        "no depende de la aprobación externa."
    ),
    ("Sol", "Virgo"): (
        "Tu identidad se construye a través del servicio, la mejora continua y la búsqueda "
        "de la excelencia en los detalles. Brillas cuando analizas, resuelves problemas "
        "prácticos y contribuyes con precisión. Tu mente discriminadora ve lo que otros pasan "
        "por alto. El desafío es el perfeccionismo excesivo que paraliza, y la tendencia "
        "a criticarte más duramente de lo que mereces."
    ),
    ("Sol", "Libra"): (
        "Tu identidad se define a través de las relaciones y la búsqueda del equilibrio justo. "
        "Brillas en contextos sociales, diplomáticos o artísticos donde puedas mediar "
        "y crear armonía. Tu sentido estético es refinado y tu empatía genuina. "
        "El desafío es la indecisión crónica y la tendencia a diluir tu identidad "
        "para mantener la paz en tus relaciones."
    ),
    ("Sol", "Escorpio"): (
        "Tu identidad es intensa, transformadora y difícil de conocer en profundidad. "
        "Brillas cuando vas hasta el fondo de cualquier asunto, cuando atraviesas crisis "
        "y resurges renovado. Tu poder de concentración y tu intuición son extraordinarios. "
        "El desafío es soltar el control, superar los celos y evitar que el miedo "
        "a la vulnerabilidad te cierre a los demás."
    ),
    ("Sol", "Sagitario"): (
        "Tu identidad es expansiva, filosófica y hambrienta de significado. Brillas cuando "
        "enseñas, viajas, exploras ideas y compartes tu visión del mundo con entusiasmo. "
        "Tu optimismo y franqueza son contagiosos. El desafío es la falta de constancia "
        "y la tendencia a predicar más de lo que practicas; también la intolerancia "
        "disfrazada de ideales."
    ),
    ("Sol", "Capricornio"): (
        "Tu identidad se forja a través del esfuerzo, la disciplina y la construcción "
        "de logros duraderos. Brillas cuando asumes responsabilidades, demuestras competencia "
        "y escales posiciones de autoridad con paciencia. Tu sentido del deber es profundo. "
        "El desafío es no sacrificar la vida emocional y personal en el altar del éxito, "
        "y aprender a recibir sin sentirlo como una deuda."
    ),
    ("Sol", "Acuario"): (
        "Tu identidad es original, humanitaria y radicalmente independiente. Brillas cuando "
        "innova, desafías lo establecido y contribuyes a causas colectivas. Tu mente "
        "puede anticipar el futuro con una claridad poco común. El desafío es la frialdad "
        "emocional y la tendencia a distanciarte de lo individual en aras de lo universal."
    ),
    ("Sol", "Piscis"): (
        "Tu identidad es fluida, compasiva y profundamente conectada con el mundo invisible. "
        "Brillas a través del arte, la espiritualidad o cualquier forma de servicio "
        "que disuelva el ego y conecte con algo mayor. Tu empatía es un don y una vulnerabilidad. "
        "El desafío es establecer límites, no evadirte de la realidad y desarrollar "
        "una identidad sólida en medio de tanta permeabilidad."
    ),

    # ── LUNA ─────────────────────────────────────────────────────────────────
    ("Luna", "Aries"): (
        "Emocionalmente eres reactivo, impulsivo y necesitas respuestas rápidas "
        "a tus necesidades. Tu mundo interior es apasionado y directo; sientes primero "
        "y piensas después. Te sientes seguro cuando puedes actuar y tomar la iniciativa. "
        "El desafío es el carácter explosivo y la dificultad para sostener el compromiso "
        "emocional a largo plazo."
    ),
    ("Luna", "Tauro"): (
        "Emocionalmente buscas estabilidad, comodidad y continuidad. Te sientes seguro "
        "cuando tus necesidades materiales y afectivas están cubiertas y el entorno es "
        "predecible. Eres de afectos profundos y leales, pero resistente al cambio emocional. "
        "El desafío es la posesividad y la dificultad para soltar cuando algo o alguien "
        "ya no sirve a tu crecimiento."
    ),
    ("Luna", "Géminis"): (
        "Emocionalmente eres curioso, necesitas variedad y la comunicación es tu forma "
        "primaria de procesar los sentimientos. Te sientes bien cuando puedes hablar, "
        "escribir o intercambiar ideas sobre lo que sientes. Tu estado de ánimo es cambiante "
        "e intelectualizado. El desafío es profundizar emocionalmente en lugar de "
        "racionalizar cada sentimiento."
    ),
    ("Luna", "Cáncer"): (
        "La Luna en su domicilio: emocionalmente eres profundo, intuitivo y con una "
        "necesidad genuina de nutrir y ser nutrido. Tienes una memoria emocional "
        "extraordinaria y el hogar es tu santuario. La familia y las raíces son centrales "
        "en tu mundo interior. El desafío es la hipersensibilidad y la tendencia a "
        "aferrarte al pasado por miedo a perder lo que amas."
    ),
    ("Luna", "Leo"): (
        "Emocionalmente necesitas reconocimiento, afecto expresivo y sentirte especial "
        "para quienes amas. Eres generoso con tus emociones y disfrutas crear alegría "
        "alrededor. Tu estado interior busca drama y colorido; lo mundano te aburre. "
        "El desafío es la dependencia del reconocimiento y la dificultad para aceptar "
        "la crítica sin sentirla como un ataque a tu valor personal."
    ),
    ("Luna", "Virgo"): (
        "Emocionalmente procesas a través del análisis y el servicio: cuando algo te "
        "preocupa, actúas, organizas u ofreces ayuda práctica. Te sientes seguro en "
        "la rutina y el orden. Tu cuidado hacia los demás es concreto y atento a los detalles. "
        "El desafío es la tendencia a la ansiedad, la autocrítica excesiva y la dificultad "
        "para recibir el cuidado que tan bien sabes dar."
    ),
    ("Luna", "Libra"): (
        "Emocionalmente buscas armonía, equilibrio y el bienestar relacional. "
        "Te sientes mejor cuando hay paz a tu alrededor y las relaciones funcionan bien. "
        "Tienes una necesidad genuina de belleza y de contextos sociales agradables. "
        "El desafío es la dependencia emocional del otro y la dificultad para tomar "
        "decisiones sin buscar validación externa."
    ),
    ("Luna", "Escorpio"): (
        "Emocionalmente eres intenso, posesivo y profundamente transformador. "
        "Sientes todo con una intensidad que pocos comprenden; los medios tonos emocionales "
        "no existen para ti. Necesitas lealtad absoluta y temes la traición por encima "
        "de casi todo. El desafío es liberar el rencor, soltar el control emocional "
        "y confiar sin necesidad de tener garantías absolutas."
    ),
    ("Luna", "Sagitario"): (
        "Emocionalmente necesitas libertad, expansión y sentido. Te sientes bien cuando "
        "exploras, viajas, aprendes o participas de algo más grande que tu cotidianidad. "
        "El optimismo es tu respuesta natural a los problemas. El desafío es la inestabilidad "
        "emocional cuando el horizonte parece cerrado, y la tendencia a huir cuando "
        "las relaciones exigen profundidad y compromiso."
    ),
    ("Luna", "Capricornio"): (
        "Emocionalmente eres contenido, reservado y sientes un deber casi inconsciente "
        "de tener todo bajo control. Muestras el afecto a través de la responsabilidad "
        "y los actos concretos más que con palabras. Te tomas la vida emocional muy en serio. "
        "El desafío es la rigidez afectiva, la dificultad para pedir ayuda y la tendencia "
        "a suprimir las emociones en lugar de procesarlas."
    ),
    ("Luna", "Acuario"): (
        "Emocionalmente eres independiente, poco convencional y procesas los sentimientos "
        "desde una perspectiva intelectual y algo distante. Necesitas espacio y libertad "
        "incluso dentro de las relaciones más íntimas. La frialdad aparente esconde "
        "una sensibilidad genuina por la humanidad en abstracto. "
        "El desafío es conectar con las emociones propias y ajenas en lo individual "
        "sin siempre elevarlas a categoría universal."
    ),
    ("Luna", "Piscis"): (
        "Emocionalmente eres poroso, empático y fácilmente influenciable por el ambiente "
        "que te rodea. Sientes lo que sienten los demás casi sin quererlo. "
        "Tu mundo interior es rico, poético y con una espiritualidad natural. "
        "El desafío es establecer límites emocionales claros, distinguir tus emociones "
        "de las ajenas y no perderte en la fusión ni en la evasión."
    ),

    # ── MERCURIO ─────────────────────────────────────────────────────────────
    ("Mercurio", "Aries"): (
        "Piensas y hablas con rapidez, directamente y sin rodeos. Tu mente va directa "
        "al punto y detesta las explicaciones largas. Eres convincente por tu energía "
        "más que por la diplomacia. El desafío es la impaciencia y no escuchar suficiente "
        "antes de responder."
    ),
    ("Mercurio", "Tauro"): (
        "Tu mente es metódica, práctica y necesita procesar a su propio ritmo. "
        "Aprendes bien lo que puedes tocar, ver o experimentar de forma concreta. "
        "Cuando llegas a una conclusión, es difícil que alguien te la cambie. "
        "El desafío es la inflexibilidad mental y la lentitud para adaptarse a ideas nuevas."
    ),
    ("Mercurio", "Géminis"): (
        "Mercurio en su domicilio: mente ágil, versátil y enamorada de las ideas. "
        "Aprendes con facilidad, conectas conceptos distantes y eres un comunicador nato. "
        "El desafío es la dispersión: tantos intereses pueden impedir la profundidad."
    ),
    ("Mercurio", "Cáncer"): (
        "Tu mente está teñida de emociones y memoria; piensas a través de imágenes, "
        "recuerdos y asociaciones afectivas. Tienes una intuición comunicativa notable "
        "y captas el subtexto emocional de las conversaciones. El desafío es la "
        "subjetividad excesiva y las decisiones basadas más en el miedo que en los datos."
    ),
    ("Mercurio", "Leo"): (
        "Piensas y te expresas con creatividad, drama y convicción. Tus palabras tienen "
        "un peso especial porque las respalda una presencia natural. Eres persuasivo "
        "y apasionado en tus argumentos. El desafío es la rigidez de opiniones "
        "y la tendencia a monopolizar la conversación."
    ),
    ("Mercurio", "Virgo"): (
        "Mercurio en exaltación y domicilio: mente analítica, precisa y capaz de procesar "
        "grandes cantidades de información con rigor. Eres un pensador crítico excepcional "
        "y excelente para el trabajo de detalle. El desafío es el sobre-análisis "
        "y el perfeccionismo que paraliza."
    ),
    ("Mercurio", "Libra"): (
        "Piensas en términos de equilibrio, justicia y comparación. Eres el mediador "
        "natural de cualquier debate; ves argumentos válidos en todas las posiciones. "
        "Comunicativamente eres elegante y diplomático. El desafío es la indecisión "
        "y la dificultad para tomar postura cuando es necesario."
    ),
    ("Mercurio", "Escorpio"): (
        "Tu mente es investigadora, penetrante y no acepta respuestas superficiales. "
        "Captas lo no dicho mejor que nadie y tienes un talento natural para la psicología "
        "y los temas profundos. El desafío es la obsesión mental y la tendencia "
        "al pensamiento secretivo o desconfiado."
    ),
    ("Mercurio", "Sagitario"): (
        "Tu mente piensa en grande, busca el panorama total y se aburre con los detalles. "
        "Eres un pensador filosófico, amante de las teorías y los grandes principios. "
        "El desafío es la imprecisión, la exageración y la dificultad para verificar "
        "los detalles que sustentan tus grandes ideas."
    ),
    ("Mercurio", "Capricornio"): (
        "Tu mente es estructurada, práctica y orientada a resultados concretos. "
        "Piensas a largo plazo y con sentido de la autoridad; tus palabras tienen peso "
        "y credibilidad. El desafío es la rigidez y la dificultad para pensar "
        "fuera de los esquemas establecidos."
    ),
    ("Mercurio", "Acuario"): (
        "Tu mente es original, sistemática y capaz de revolucionar ideas establecidas. "
        "Piensas de forma no lineal y anticipas tendencias que otros aún no ven. "
        "El desafío es la frialdad intelectual y la tendencia a desconectarte "
        "emocionalmente cuando el pensamiento se vuelve abstracto."
    ),
    ("Mercurio", "Piscis"): (
        "Tu mente funciona a través de la intuición, la imagen y la asociación poética "
        "más que por la lógica lineal. Eres creativo, empático y captas el estado de "
        "ánimo de las situaciones de forma casi telepática. El desafío es la imprecisión, "
        "la dificultad para fijar ideas y la confusión entre lo imaginado y lo real."
    ),

    # ── VENUS ─────────────────────────────────────────────────────────────────
    ("Venus", "Aries"): (
        "Amas con intensidad y rapidez; te enamoras de golpe y necesitas el estímulo "
        "de la conquista. En el amor eres apasionado, directo y algo impaciente. "
        "El desafío es la impaciencia con los procesos lentos y la tendencia a perder "
        "el interés una vez superada la fase de conquista."
    ),
    ("Venus", "Tauro"): (
        "Venus en domicilio: aprecias la belleza sensorial, la lealtad y los placeres "
        "materiales. En el amor eres constante, afectuoso y buscas seguridad. "
        "Tienes un sentido estético refinado y un don para crear ambientes hermosos. "
        "El desafío es la posesividad y la resistencia a los cambios en la relación."
    ),
    ("Venus", "Géminis"): (
        "Amas la conversación, la variedad y la conexión mental. En el amor necesitas "
        "un compañero que sea también amigo e interlocutor intelectual. "
        "Eres encantador, adaptable y con mucho ingenio. El desafío es la inconstancia "
        "y la dificultad para comprometerse cuando el entorno ofrece muchas opciones."
    ),
    ("Venus", "Cáncer"): (
        "Amas con profundidad emocional y necesitas seguridad y reciprocidad. "
        "Eres extremadamente cariñoso y tienes un instinto nutridor muy desarrollado. "
        "El hogar y la familia son el escenario de tus mejores expresiones afectivas. "
        "El desafío es el apego excesivo y la tendencia a aferrarte a relaciones "
        "que ya deberían finalizar."
    ),
    ("Venus", "Leo"): (
        "Amas de forma dramática, generosa y teatral. En el amor necesitas admiración "
        "y expresas el afecto de manera grandiosa. Eres fiel y apasionado cuando "
        "sientes que eres el centro del mundo de tu pareja. El desafío es la vanidad "
        "y la necesidad de ser el protagonista incluso en la relación."
    ),
    ("Venus", "Virgo"): (
        "Muestras el afecto a través de los actos de servicio y la atención a los detalles "
        "del otro. Eres selectivo en el amor, cauteloso y buscas la perfección en la pareja. "
        "El desafío es la hipercrítica que destruye lo que no es perfecto, "
        "y la dificultad para expresar el afecto de forma espontánea y sin condiciones."
    ),
    ("Venus", "Libra"): (
        "Venus en domicilio: el amor es tu elemento natural. Buscas la pareja ideal, "
        "la relación armoniosa y el romance elegante. Eres diplomático, considerado "
        "y capaz de crear belleza en tu entorno. El desafío es la dependencia del otro "
        "y la tendencia a evitar los conflictos necesarios para el crecimiento."
    ),
    ("Venus", "Escorpio"): (
        "Amas con una intensidad que puede asustar: todo o nada. Buscas la fusión total, "
        "la lealtad absoluta y la transformación a través del amor. Eres apasionado "
        "y profundamente sensual. El desafío es los celos, el deseo de control "
        "y la dificultad para perdonar las traiciones."
    ),
    ("Venus", "Sagitario"): (
        "Amas la libertad, la aventura y el crecimiento compartido. En la relación "
        "necesitas espacio para seguir siendo tú mismo. Eres generoso, optimista "
        "y muy atractivo para quienes comparten tu amor por la vida. "
        "El desafío es el miedo al compromiso y la tendencia a idealizar al amado "
        "hasta que la realidad lo desmonta."
    ),
    ("Venus", "Capricornio"): (
        "Amas con seriedad, lealtad y un sentido práctico de la relación. "
        "Buscas una pareja con quien construir algo duradero y confiable. "
        "El afecto lo demuestras con actos y responsabilidad más que con palabras. "
        "El desafío es la frialdad emocional aparente y la dificultad para ser "
        "espontáneo y vulnerable."
    ),
    ("Venus", "Acuario"): (
        "Amas la amistad dentro de la relación y valoras la independencia mutua. "
        "Buscas conexiones únicas, poco convencionales y estimulantes intelectualmente. "
        "El desafío es la distancia emocional y la tendencia a intelectualizar "
        "los sentimientos en lugar de vivirlos."
    ),
    ("Venus", "Piscis"): (
        "Venus en exaltación: amas de forma incondicional, romántica y casi mística. "
        "Estás dispuesto a sacrificarte por el amor y tienes una capacidad de entrega "
        "poco común. El desafío es idealizar al otro hasta el punto de no ver "
        "la realidad, o convertirte en mártir de una relación insana."
    ),

    # ── MARTE ─────────────────────────────────────────────────────────────────
    ("Marte", "Aries"): (
        "Marte en domicilio: energía desbordante, directa y pionera. Actúas antes "
        "de pensar, lideras con el cuerpo y la voluntad. Eres competitivo y valiente. "
        "El desafío es controlar la impulsividad y la agresividad cuando no se sale "
        "con la tuya."
    ),
    ("Marte", "Tauro"): (
        "Tu energía es lenta para arrancar pero prácticamente imparable una vez en marcha. "
        "Trabajas con persistencia y construyes con los materiales disponibles. "
        "Eres tenaz y muy productivo en las cosas que valoras. El desafío es la "
        "terquedad y los arranques de ira cuando algo viola tu sentido de seguridad."
    ),
    ("Marte", "Géminis"): (
        "Tu energía va hacia las ideas, las palabras y las conexiones múltiples. "
        "Eres ágil mentalmente y puedes hacer varias cosas a la vez. El debate "
        "y la argumentación son tu forma de acción. El desafío es la dispersión "
        "y la dificultad para sostener el esfuerzo en una sola dirección."
    ),
    ("Marte", "Cáncer"): (
        "Tu energía se activa cuando algo amenaza tu hogar o tu familia. Actúas "
        "movido por las emociones más que por la razón, y tu resistencia es notable "
        "cuando defiendes lo que amas. El desafío es la acción indirecta, los modos "
        "pasivo-agresivos y la dificultad para confrontar directamente."
    ),
    ("Marte", "Leo"): (
        "Tu energía es creativa, dramática y necesita un escenario para brillar. "
        "Actúas con convicción y liderazgo natural; eres valiente cuando se trata "
        "de defender tu dignidad. El desafío es el orgullo herido que puede "
        "convertir un desacuerdo menor en una batalla épica."
    ),
    ("Marte", "Virgo"): (
        "Tu energía va hacia el perfeccionamiento, el trabajo técnico y el servicio. "
        "Eres meticuloso, eficiente y capaz de un esfuerzo sostenido y preciso. "
        "El desafío es la tendencia a malgastar energía en la autocrítica "
        "y en detalles que no cambian el resultado final."
    ),
    ("Marte", "Libra"): (
        "Tu energía se orienta hacia la justicia, la mediación y el equilibrio. "
        "Actúas cuando percibes una injusticia flagrante. Puedes ser un negociador "
        "de hierro envuelto en seda diplomática. El desafío es la indecisión que "
        "paraliza la acción y la tendencia a la acción pasivo-agresiva."
    ),
    ("Marte", "Escorpio"): (
        "Marte en domicilio: energía intensa, estratégica y con una perseverancia "
        "casi sobrehumana. Cuando te propones algo, los obstáculos solo aumentan "
        "tu determinación. Tienes un magnetismo sexual poderoso. El desafío es "
        "el rencor, la venganza y el uso del poder de forma destructiva."
    ),
    ("Marte", "Sagitario"): (
        "Tu energía es entusiasta, filosófica y necesita una causa grande para "
        "comprometerse. Actúas movido por los ideales y tienes una audacia "
        "que inspira a otros. El desafío es la inconstancia y el exceso de "
        "optimismo que subestima los obstáculos reales."
    ),
    ("Marte", "Capricornio"): (
        "Marte en exaltación: energía disciplinada, estratégica y orientada "
        "al logro a largo plazo. Trabajas duro, con paciencia y sin desperdiciar "
        "esfuerzos. El poder, la autoridad y el reconocimiento social son tus "
        "motivaciones profundas. El desafío es la frialdad y el utilitarismo "
        "que puede deshumanizar las relaciones."
    ),
    ("Marte", "Acuario"): (
        "Tu energía va hacia la innovación, la rebeldía constructiva y las causas "
        "colectivas. Actúas por principios más que por instinto. Eres original "
        "en tu forma de abordar los conflictos. El desafío es la frialdad "
        "y la tendencia a dispersar la energía en demasiados frentes ideológicos."
    ),
    ("Marte", "Piscis"): (
        "Tu energía es difusa, compasiva y con dificultad para definir objetivos "
        "claros. Actúas movido por la inspiración o la empatía más que por la ambición. "
        "Tienes una resistencia silenciosa notable. El desafío es la pasividad, "
        "la evasión y la dificultad para defender tus propios intereses directamente."
    ),

    # ── JÚPITER ───────────────────────────────────────────────────────────────
    ("Júpiter", "Aries"): (
        "La expansión llega a través de la acción atrevida, el liderazgo y la iniciativa. "
        "Tienes suerte cuando actúas con valentía y confías en tu instinto. "
        "Puedes ser un pionero en tu campo. El desafío es el exceso de confianza "
        "y la tendencia a asumir más riesgos de los convenientes."
    ),
    ("Júpiter", "Tauro"): (
        "La abundancia llega a través de la paciencia, el trabajo constante y la conexión "
        "con los valores materiales y naturales. Tienes un don para crear riqueza "
        "de forma sostenible. El desafío es el exceso en los placeres materiales "
        "y la resistencia a soltar lo que ya no da más de sí."
    ),
    ("Júpiter", "Géminis"): (
        "La expansión llega a través del conocimiento, la comunicación y la variedad "
        "de experiencias intelectuales. Aprendes rápido y conectas ideas de campos "
        "distintos con brillantez. El desafío es la superficialidad y la dispersión "
        "que impide profundizar en lo que realmente importa."
    ),
    ("Júpiter", "Cáncer"): (
        "Júpiter en exaltación: la abundancia llega a través del hogar, la familia "
        "y el cuidado emocional. Tienes una generosidad genuina con quienes amas "
        "y una capacidad nutritiva que atrae protección y bienestar. "
        "El desafío es el exceso de indulgencia emocional y el apego exagerado."
    ),
    ("Júpiter", "Leo"): (
        "La expansión llega a través de la creatividad, el liderazgo y la expresión "
        "generosa de tus talentos. Tienes carisma natural y la capacidad de inspirar "
        "a otros. El desafío es el ego inflado y la necesidad de protagonismo "
        "que puede eclipsar la genuina generosidad."
    ),
    ("Júpiter", "Virgo"): (
        "La expansión llega a través del servicio, la mejora de procesos y el trabajo "
        "bien hecho. Eres abundante cuando aplicas tus conocimientos de forma práctica. "
        "El desafío es el exceso de análisis que paraliza la expansión "
        "y el perfeccionismo que convierte la abundancia en escasez."
    ),
    ("Júpiter", "Libra"): (
        "La expansión llega a través de las relaciones, las asociaciones y el arte. "
        "Tienes talento para crear alianzas beneficiosas y para mediar con justicia. "
        "El desafío es la tendencia a la indolencia y a depender del otro "
        "para que la expansión se materialice."
    ),
    ("Júpiter", "Escorpio"): (
        "La expansión llega a través de la transformación profunda, la investigación "
        "y el acceso a recursos ajenos. Tienes talento para los negocios de fondo "
        "y los asuntos que otros consideran tabú. El desafío es el exceso de "
        "intensidad y la obsesión que convierte el crecimiento en compulsión."
    ),
    ("Júpiter", "Sagitario"): (
        "Júpiter en domicilio: optimismo desbordante, visión filosófica y una suerte "
        "que acompaña los viajes y las grandes aventuras. Tienes una fe genuina en "
        "la vida que se convierte en profecía autocumplida. El desafío es el exceso "
        "de confianza que promete más de lo que puede cumplir."
    ),
    ("Júpiter", "Capricornio"): (
        "La expansión llega a través del esfuerzo disciplinado y la construcción "
        "paciente de estructuras sólidas. Eres ambicioso y estratégico. "
        "El desafío es la excesiva precaución que impide aprovechar las oportunidades "
        "y la tendencia a reducir la abundancia a mero éxito material."
    ),
    ("Júpiter", "Acuario"): (
        "La expansión llega a través de la innovación, los grupos y las causas "
        "humanitarias. Tienes visión de futuro y capacidad para llevar ideas "
        "revolucionarias al mundo. El desafío es la dispersión en ideales "
        "demasiado abstractos y la dificultad para aterrizar la visión."
    ),
    ("Júpiter", "Piscis"): (
        "Júpiter en domicilio: expansión a través de la espiritualidad, el arte "
        "y la compasión. Tienes una fe profunda y una generosidad casi sin límites. "
        "Tu intuición puede guiarte a oportunidades invisibles para otros. "
        "El desafío es el escapismo y la tendencia a dar sin discernimiento."
    ),

    # ── SATURNO ───────────────────────────────────────────────────────────────
    ("Saturno", "Aries"): (
        "Las lecciones de vida giran en torno a desarrollar la identidad propia "
        "sin depender de la validación. Aprendes a actuar con iniciativa a pesar del miedo. "
        "Puedes sentir frenos internos para afirmar tu voluntad. "
        "La madurez trae una valentía real, ganada a pulso."
    ),
    ("Saturno", "Tauro"): (
        "Las lecciones giran en torno a la seguridad material y los valores profundos. "
        "Construyes lentamente pero con una solidez que perdura. Puedes pasar por "
        "períodos de escasez que te enseñan el verdadero valor de lo que posees. "
        "La madurez trae una abundancia ganada con disciplina."
    ),
    ("Saturno", "Géminis"): (
        "Las lecciones giran en torno a la comunicación, el aprendizaje y el pensamiento. "
        "Puedes sentir bloqueos para expresarte o inseguridad intelectual. "
        "Con tiempo desarrollas una mente rigurosa y una comunicación de alta precisión. "
        "La madurez trae autoridad intelectual."
    ),
    ("Saturno", "Cáncer"): (
        "Las lecciones más profundas están en el hogar, la familia y la vulnerabilidad emocional. "
        "Puede haber frialdad o distancia afectiva en la crianza recibida. "
        "Aprendes a construir seguridad interna independiente del entorno familiar. "
        "La madurez trae una capacidad de cuidado profunda y bien fundamentada."
    ),
    ("Saturno", "Leo"): (
        "Las lecciones giran en torno al reconocimiento, la creatividad y la confianza en uno mismo. "
        "Puedes sentir que nunca eres suficientemente brillante o visible. "
        "Con tiempo desarrollas una autoridad creativa genuina y un liderazgo maduro. "
        "La madurez trae un ego sano y una dignidad ganada a través de la prueba."
    ),
    ("Saturno", "Virgo"): (
        "Las lecciones giran en torno al trabajo, la salud y el perfeccionismo. "
        "Puedes exigirte tanto que nunca nada es suficiente. Con tiempo desarrollas "
        "una maestría técnica notable y un sentido del servicio muy exigente y eficaz. "
        "La madurez trae la paz de hacer bien sin necesitar que sea perfecto."
    ),
    ("Saturno", "Libra"): (
        "Saturno en exaltación: las lecciones giran en torno a las relaciones y la justicia. "
        "Aprendes que las relaciones maduras requieren compromiso real, no solo armonía superficial. "
        "Con tiempo te conviertes en un árbitro justo y un socio de profunda fiabilidad. "
        "La madurez trae relaciones sólidas construidas sobre valores compartidos."
    ),
    ("Saturno", "Escorpio"): (
        "Las lecciones más profundas están en el poder, la sexualidad, las pérdidas "
        "y la transformación. Puede haber experiencias de traición o pérdida que forjan "
        "una fortaleza interior excepcional. Con tiempo desarrollas una maestría "
        "para manejar los recursos y los procesos de cambio profundo."
    ),
    ("Saturno", "Sagitario"): (
        "Las lecciones giran en torno a la fe, la filosofía y la expansión. "
        "Puedes sentir restricciones para viajar, estudiar o desarrollar tu visión del mundo. "
        "Con tiempo construyes una filosofía sólida y bien fundamentada, lejos del dogmatismo. "
        "La madurez trae sabiduría real, ganada a través de la experiencia y no solo de la fe."
    ),
    ("Saturno", "Capricornio"): (
        "Saturno en domicilio: disciplina, ambición y una comprensión profunda de las estructuras "
        "del mundo. Las lecciones giran en torno a la responsabilidad y el precio del éxito. "
        "Puedes cargar con demasiadas obligaciones. Con tiempo construyes una autoridad "
        "y un legado genuinos, pero aprendes también a disfrutar el camino."
    ),
    ("Saturno", "Acuario"): (
        "Saturno en domicilio: las lecciones giran en torno al grupo, la innovación "
        "y la responsabilidad colectiva. Puedes sentir tensión entre la necesidad "
        "de libertad y la de estructura. Con tiempo te conviertes en arquitecto "
        "de sistemas nuevos que duran porque están bien construidos."
    ),
    ("Saturno", "Piscis"): (
        "Las lecciones giran en torno a los límites de la compasión, la espiritualidad "
        "y lo invisible. Puedes sentir que cargas con el dolor del mundo. "
        "Con tiempo desarrollas una espiritualidad madura y una disciplina interior "
        "que convierte la sensibilidad en fortaleza real."
    ),

    # ── URANO (generacional con matiz personal) ───────────────────────────────
    ("Urano", "Aries"): "Generación (2011-2018) con un impulso colectivo de romper moldes de identidad y liderazgo. En lo personal: la necesidad de cambio se manifiesta de forma impulsiva e inesperada.",
    ("Urano", "Tauro"): "Generación (2018-2026) que transforma la economía, los valores y la relación con la naturaleza. En lo personal: los cambios llegan a través de la seguridad material y los sistemas de valor.",
    ("Urano", "Géminis"): "Generación que revolucionó la comunicación y el pensamiento. En lo personal: mente muy original con ideas que adelantan su tiempo.",
    ("Urano", "Cáncer"): "Generación que transformó las estructuras familiares y el concepto de hogar. En lo personal: los cambios llegan a través de la familia y la memoria colectiva.",
    ("Urano", "Leo"): "Generación que revolucionó la creatividad, el entretenimiento y la identidad colectiva. En lo personal: necesidad de ser único y brillar de forma original.",
    ("Urano", "Virgo"): "Generación que transformó el trabajo, la salud y los sistemas de servicio. En lo personal: innovación a través del análisis y la mejora técnica.",
    ("Urano", "Libra"): "Generación (1968-1975) que transformó el matrimonio, las relaciones y la justicia. En lo personal: relaciones poco convencionales y búsqueda de igualdad.",
    ("Urano", "Escorpio"): "Generación (1975-1981) que transformó el poder, la sexualidad y los tabúes. En lo personal: cambios profundos e inesperados en los temas de control y regeneración.",
    ("Urano", "Sagitario"): "Generación (1981-1988) que revolucionó la religión, la educación y los viajes. En lo personal: filosofía de vida original y rechazo al dogma.",
    ("Urano", "Capricornio"): "Generación (1988-1996) que transforma las estructuras de poder y la autoridad. En lo personal: ambición original que rompe con las jerarquías establecidas.",
    ("Urano", "Acuario"): "Generación (1996-2003) nacida en la era digital. En lo personal: mente tecnológica, revolucionaria y con visión humanitaria.",
    ("Urano", "Piscis"): "Generación (2003-2010) que transforma la espiritualidad y lo colectivo inconsciente. En lo personal: intuición revolucionaria y compasión inesperada.",

    # ── NEPTUNO (generacional) ────────────────────────────────────────────────
    ("Neptuno", "Capricornio"): "Generación (1984-1998) que disuelve las estructuras de poder y el materialismo institucional. Ilusiones colectivas sobre el éxito y la autoridad.",
    ("Neptuno", "Acuario"): "Generación (1998-2012) que disuelve las fronteras entre lo digital y lo real, y sueña con una humanidad unida. Ilusiones colectivas sobre la tecnología como salvación.",
    ("Neptuno", "Piscis"): "Generación (2012-2025) que disuelve los velos entre dimensiones; espiritualidad, arte y compasión global. Neptuno en casa propia, máxima potencia espiritual y riesgo de evasión colectiva.",
    ("Neptuno", "Aries"): "Generación (2025-2039) que disuelve los egos colectivos y sueña con nuevas formas de liderazgo espiritual.",

    # ── PLUTÓN (generacional) ─────────────────────────────────────────────────
    ("Plutón", "Libra"): "Generación (1971-1984) que transforma profundamente las relaciones, el matrimonio y la justicia social. Poder y sombra en las asociaciones.",
    ("Plutón", "Escorpio"): "Generación (1984-1995) marcada por el SIDA, la muerte y la transformación de tabúes. Intensidad psicológica colectiva y poder regenerador.",
    ("Plutón", "Sagitario"): "Generación (1995-2008) que transforma la religión, la filosofía y la globalización. Fundamentalismo y búsqueda de sentido como fuerzas opuestas.",
    ("Plutón", "Capricornio"): "Generación (2008-2024) que transforma las estructuras de poder, el capitalismo y la autoridad. Crisis sistémicas como catalizadores de regeneración.",
    ("Plutón", "Acuario"): "Generación (2024-2044) que transforma la tecnología, la humanidad y los sistemas colectivos. El poder del dato y la revolución digital como fuerza transformadora.",
}

# ─────────────────────────────────────────────────────────────────────────────
# PLANETA EN CASA
# ─────────────────────────────────────────────────────────────────────────────

PLANET_IN_HOUSE: dict[tuple[str, int], str] = {

    # SOL en casas
    ("Sol", 1): "Tu identidad y vitalidad se expresan directamente en la personalidad. Proyectas confianza y autoridad natural; los demás te ven tal como tú te ves a ti mismo. Tienes un fuerte deseo de afirmar tu individualidad.",
    ("Sol", 2): "Tu ego se nutre de la seguridad material. Buscas el reconocimiento a través de lo que posees y produces. Tienes talento para generar recursos pero necesitas cuidar de no identificarte en exceso con lo material.",
    ("Sol", 3): "Tu propósito se expresa a través de la comunicación, el aprendizaje y los vínculos cercanos. Brillas en la escritura, la enseñanza o cualquier medio de difusión de ideas. Los hermanos pueden ser figuras muy importantes.",
    ("Sol", 4): "Tu identidad está profundamente arraigada en el hogar y la familia. Buscas reconocimiento en el ámbito privado y tus raíces determinan quién eres. Puede haber un padre muy dominante o ausente que moldea tu carácter.",
    ("Sol", 5): "Brillas en la creatividad, el romance y la autoexpresión. El juego, los hijos y el arte son áreas donde tu vitalidad fluye naturalmente. Necesitas un escenario donde poder brillar y ser reconocido.",
    ("Sol", 6): "Tu vitalidad se expresa a través del trabajo cotidiano y el servicio. Buscas el reconocimiento en el ámbito laboral y en la eficiencia de lo que haces. La salud y los hábitos son áreas de atención constante.",
    ("Sol", 7): "Buscas afirmar tu identidad a través de las relaciones. El otro es un espejo poderoso. Puedes atraer parejas fuertes o dominantes. Brillas en el trabajo conjunto y las asociaciones estratégicas.",
    ("Sol", 8): "Tu propósito de vida implica la transformación profunda. Atraes situaciones de crisis que te obligan a renacer. Tienes talento para los temas de psicología, herencias, sexualidad y lo oculto.",
    ("Sol", 9): "Brillas cuando enseñas, viajas o exploras grandes sistemas de pensamiento. La filosofía, la religión y la educación superior son campos naturales. Buscas el sentido de la vida a través de la expansión constante.",
    ("Sol", 10): "El Sol está en la cima de la carta: la carrera y el reconocimiento público son áreas centrales. Tienes vocación de autoridad y liderazgo visible. Tu identidad se construye a través de lo que logras en el mundo.",
    ("Sol", 11): "Brillas en los grupos, las causas colectivas y la amistad. Tu propósito está ligado al futuro y a las comunidades que eliges. Eres un activador de redes y un referente dentro de tus círculos.",
    ("Sol", 12): "Tu propósito de vida tiene una dimensión espiritual o invisible. Puedes brillar en contextos de retiro, creatividad en soledad o trabajo con los marginados. El ego necesita aprender a disolverse antes de realizarse.",

    # LUNA en casas
    ("Luna", 1): "Las emociones se expresan directamente en el cuerpo y la apariencia. Eres muy reactivo al ambiente y los demás perciben tu estado interior fácilmente. Tu imagen fluctúa según tu estado emocional.",
    ("Luna", 2): "La seguridad emocional está ligada a la seguridad material. Tus ingresos pueden fluctuar con tu estado de ánimo. Tienes una relación emocional profunda con el dinero y las posesiones.",
    ("Luna", 3): "El pensamiento es intuitivo y emotivo más que lógico. Tienes una memoria excelente para los detalles emocionales y conversacionales. Los hermanos y vecinos juegan un papel afectivo importante.",
    ("Luna", 4): "La Luna en su casa natural: el hogar y la familia son el centro de tu mundo emocional. Necesitas un refugio seguro para funcionar bien. El pasado y la madre tienen una influencia profunda y duradera.",
    ("Luna", 5): "Las emociones se expresan a través de la creatividad, el juego y el romance. Eres muy afectuoso con los hijos. Tu vida amorosa es intensa y el corazón guía más que la razón.",
    ("Luna", 6): "Las emociones afectan directamente la salud. El trabajo cotidiano necesita ser emocionalmente satisfactorio para que funciones bien. Tienes un instinto de cuidado muy desarrollado hacia compañeros y subordinados.",
    ("Luna", 7): "Buscas la seguridad emocional a través de la pareja. Las relaciones son muy importantes para tu bienestar. Puedes atraer parejas emocionalmente dependientes o necesitadas de cuidado.",
    ("Luna", 8): "Las emociones más profundas están relacionadas con la pérdida, la transformación y lo tabú. Tienes una intuición muy desarrollada sobre las motivaciones ocultas. Las herencias y los bienes compartidos pueden ser fluctuantes.",
    ("Luna", 9): "Las emociones se nutren de la expansión: viajes, estudio, filosofía. Tienes una fe instintiva y un amor por las culturas lejanas. Las experiencias de apertura mental alimentan tu mundo interior.",
    ("Luna", 10): "Las emociones están conectadas con la carrera y la reputación pública. El éxito profesional tiene una carga emocional muy alta. Puedes ser una figura maternal o muy visible en tu campo.",
    ("Luna", 11): "Las emociones se nutren de los grupos y las amistades. Necesitas sentirte parte de una comunidad para sentirte bien. Tienes una intuición notable sobre las tendencias sociales.",
    ("Luna", 12): "Las emociones operan en las capas más profundas e inconscientes. Puedes tener una vida interior muy rica que pocas personas conocen. El retiro y la soledad son necesarios para tu equilibrio emocional.",

    # MERCURIO en casas
    ("Mercurio", 1): "La mente y el habla son parte central de tu personalidad. Te presentas como intelectual, comunicativo y ágil. El aprendizaje continuo es parte de tu identidad.",
    ("Mercurio", 2): "Haces dinero con la mente: escritura, ventas, enseñanza o comercio. El dinero llega a través de las ideas y la comunicación. Los valores son objeto de reflexión constante.",
    ("Mercurio", 3): "Mercurio en casa propia: mente brillante, ágil y comunicativa. Los hermanos, los estudios y los viajes cortos son áreas favorecidas. Excelente para la escritura y el periodismo.",
    ("Mercurio", 4): "Piensas mucho en el hogar, la familia y el pasado. Puede haber mucho intercambio intelectual en casa. Tu mente fue muy influenciada por el entorno familiar de la infancia.",
    ("Mercurio", 5): "La creatividad es intelectual: escritura creativa, juegos de ingenio, educación de los hijos. El romance también tiene una fuerte dimensión mental.",
    ("Mercurio", 6): "Mente orientada a los procesos, la salud y el trabajo cotidiano. Excelente para la medicina, la artesanía o cualquier trabajo que requiera precisión mental y manual.",
    ("Mercurio", 7): "Las relaciones son intelectuales y comunicativas. Buscas una pareja con quien hablar y aprender. El abogado, el asesor o el negociador son roles naturales.",
    ("Mercurio", 8): "Mente investigadora, interesada en lo oculto, la psicología y los tabúes. Tienes talento para la investigación profunda, el análisis financiero y la terapia.",
    ("Mercurio", 9): "La mente busca la verdad grande: filosofía, religión, leyes o culturas extranjeras. Excelente para la academia, la publicación o la enseñanza de alto nivel.",
    ("Mercurio", 10): "La carrera implica la comunicación, la escritura o la docencia. Tu reputación pública está ligada a tus ideas. El periodismo, la política o la educación son campos naturales.",
    ("Mercurio", 11): "Las ideas fluyen mejor en grupo. Tienes talento para las redes, los proyectos colectivos y el activismo intelectual. Los amigos son fuente de información y estimulación mental.",
    ("Mercurio", 12): "La mente trabaja en soledad y profundidad. Puedes tener talento para la escritura privada, la investigación en retiro o la psicología. Algunos pensamientos quedan en el reino interior sin expresarse.",

    # VENUS en casas
    ("Venus", 1): "Tienes un encanto natural y una apariencia atractiva. El amor por la belleza es visible en tu presencia. Las relaciones son muy importantes para tu sentido de identidad.",
    ("Venus", 2): "Venus en casa propia: talento natural para ganar dinero y atraer recursos. El placer material es genuino. Tienes gusto estético y sabes el valor de las cosas.",
    ("Venus", 3): "Hablas con encanto y elegancia. Las relaciones con hermanos y vecinos son armoniosas. Tienes talento para la poesía, el diseño editorial o cualquier forma de comunicación estética.",
    ("Venus", 4): "El hogar es un espacio de belleza y armonía. Relación afectiva con la familia muy desarrollada. Puede haber una madre muy amorosa o muy apreciada.",
    ("Venus", 5): "Venus en casa propia del amor: romanticismo, placer artístico y amor por los niños. La vida amorosa es un área de gran importancia y disfrute. Tienes talento creativo notable.",
    ("Venus", 6): "Haces el trabajo cotidiano con gracia y armonía. El entorno laboral necesita ser agradable. Tienes talento para las profesiones de cuidado o que impliquen belleza y servicio.",
    ("Venus", 7): "Venus en casa propia: las relaciones son armoniosas y centrales en tu vida. Tienes talento para las asociaciones y el matrimonio. Atraes parejas bellas, afectuosas o artísticas.",
    ("Venus", 8): "El amor tiene una profundidad transformadora. Las relaciones íntimas te cambian profundamente. Puede haber beneficio a través de herencias o bienes del cónyuge.",
    ("Venus", 9): "El amor por la filosofía, los viajes y las culturas lejanas es genuino. Puedes encontrar pareja en el extranjero o a través de estudios. El arte y la espiritualidad son fuentes de placer.",
    ("Venus", 10): "La carrera está relacionada con el arte, la diplomacia o las relaciones públicas. Tienes encanto profesional y una reputación positiva. El éxito puede llegar a través de la belleza o el trato con el público.",
    ("Venus", 11): "Las amistades son afectuosas y duraderas. Tienes talento para crear comunidad y armonía en los grupos. El amor puede nacer en círculos de amigos.",
    ("Venus", 12): "El amor tiene una dimensión espiritual o sacrificada. Puedes amar en secreto o sufrir por amores que no pueden expresarse plenamente. El arte en soledad es una fuente de belleza profunda.",

    # MARTE en casas
    ("Marte", 1): "Energía directa, cuerpo atlético y personalidad asertiva. Te presentas con fuerza y determinación. La acción y la iniciativa son parte de tu identidad.",
    ("Marte", 2): "Energía orientada a ganar dinero y defender lo que posees. Puedes ser muy productivo pero también impulsivo con el gasto. La seguridad material motiva tus acciones.",
    ("Marte", 3): "Comunicación directa, a veces agresiva. La mente actúa antes de que las palabras estén listas. Excelente para el debate, el periodismo de campo o la conducción.",
    ("Marte", 4): "La energía se activa en el hogar: conflictos familiares o mucha actividad doméstica. Puedes ser protector feroz de tu familia. El padre puede haber sido una figura enérgica.",
    ("Marte", 5): "Energía creativa desbordante y vida amorosa intensa. Competitivo en el juego y apasionado en el romance. Posibles conflictos con los hijos o a través de ellos.",
    ("Marte", 6): "Gran capacidad de trabajo y energía para el día a día. Excelente para profesiones que requieran esfuerzo físico o técnico. Atención a la salud: el exceso de trabajo puede generar inflamaciones.",
    ("Marte", 7): "Las relaciones tienen tensión y pasión. Puedes atraer parejas dominantes o conflictivas. También indica el tipo de competidor o rival que encuentras en la vida.",
    ("Marte", 8): "Energía transformadora intensa. Atraes crisis que obligan a la renovación. Talento para la investigación, la cirugía o cualquier trabajo que implique entrar en lo profundo.",
    ("Marte", 9): "Energía filosófica y aventurera. Defiendes tus ideas con pasión. Los viajes pueden ser intensos o peligrosos si no hay precaución. Excelente para la abogacía o el activismo.",
    ("Marte", 10): "Gran ambición y energía para el éxito profesional. Lideras con fuerza y determinación en la carrera. Puedes destacar en campos que requieran liderazgo o acción.",
    ("Marte", 11): "Energía orientada a los grupos y causas colectivas. Puedes ser el activista o el líder de movimientos. Las amistades pueden ser competitivas o muy dinámicas.",
    ("Marte", 12): "La energía actúa en lo invisible: motivaciones ocultas, enemigos secretos, trabajo entre bastidores. Puede haber ira reprimida. El ejercicio y la soledad son válvulas necesarias.",

    # JÚPITER en casas
    ("Júpiter", 1): "Presencia expansiva, optimista y generosa. La vida en general fluye con relativa facilidad. Tendencia al exceso en el cuerpo; cuidado con el peso o los excesos materiales.",
    ("Júpiter", 2): "La abundancia material llega con relativa facilidad. Tienes fe en los recursos y eso los atrae. Generoso con el dinero aunque a veces demasiado.",
    ("Júpiter", 3): "Mente expansiva, curiosa y con facilidad para la comunicación y el aprendizaje. Los hermanos o vecinos pueden ser una fuente de suerte. Excelente para la escritura y la enseñanza.",
    ("Júpiter", 4): "Hogar y familia son fuentes de abundancia y protección. Tendencia a tener una familia grande o muy generosa. La segunda mitad de la vida suele traer estabilidad doméstica creciente.",
    ("Júpiter", 5): "Gran suerte en el amor, la creatividad y los hijos. Vida amorosa rica y placentera. Los juegos de azar pueden ser favorables con moderación.",
    ("Júpiter", 6): "Suerte en el trabajo y la salud. El ambiente laboral suele ser amplio y favorable. Tienes fe en los procesos de mejora. Cuidado con el exceso de trabajo o los hábitos exagerados.",
    ("Júpiter", 7): "Las relaciones traen expansión y suerte. La pareja suele ser generosa, filosófica o muy viajera. Las asociaciones son fuente de crecimiento.",
    ("Júpiter", 8): "La expansión llega a través de transformaciones profundas, herencias o recursos de otros. Tienes suerte en los asuntos de inversión y gestión de crisis.",
    ("Júpiter", 9): "Júpiter en casa propia: gran suerte en los viajes, los estudios superiores y la filosofía. Eres un eterno explorador del saber. La vida te lleva lejos geográfica o mentalmente.",
    ("Júpiter", 10): "La carrera está bendecida con crecimiento y reconocimiento. Tienes vocación de liderazgo y una reputación que se expande. El éxito llega pero requiere no caer en la arrogancia.",
    ("Júpiter", 11): "La suerte llega a través de los grupos y las amistades. Tus redes son extensas y generosas. Los proyectos colectivos se expanden. Las esperanzas suelen cumplirse.",
    ("Júpiter", 12): "La expansión ocurre en lo invisible: espiritualidad, retiro, arte interior. Eres protegido por fuerzas que no siempre puedes ver. La generosidad silenciosa es tu mayor virtud.",

    # SATURNO en casas
    ("Saturno", 1): "La personalidad es seria, contenida y madura desde joven. Puede haber una infancia marcada por la responsabilidad temprana. Con el tiempo desarrollas una autoridad real y una presencia de confianza.",
    ("Saturno", 2): "Las lecciones de la seguridad material son constantes. Pueden existir períodos de escasez que enseñan el valor del ahorro y la disciplina. Con tiempo construyes una base económica sólida.",
    ("Saturno", 3): "El aprendizaje y la comunicación requieren esfuerzo adicional. Puede haber dificultades tempranas con el lenguaje o los estudios básicos. Con tiempo te conviertes en un comunicador preciso y de gran profundidad.",
    ("Saturno", 4): "Las raíces familiares pesan con fuerza, a veces con dolor. Puede haber un entorno doméstico frío o muy estructurado en la infancia. Con tiempo construyes un hogar sólido basado en lo que tú eliges.",
    ("Saturno", 5): "Las limitaciones en la creatividad y el amor pueden sentirse desde joven. La diversión requiere un permiso interno que a veces falta. Con tiempo desarrollas una creatividad disciplinada y un amor profundamente comprometido.",
    ("Saturno", 6): "El trabajo es una lección constante de responsabilidad. La salud requiere atención y disciplina. Con tiempo te conviertes en un profesional de excepcional fiabilidad y exigencia.",
    ("Saturno", 7): "Las relaciones llegan tarde o implican responsabilidades importantes. La pareja puede ser mayor o traer lecciones de madurez. Con tiempo construyes relaciones sólidas basadas en el compromiso real.",
    ("Saturno", 8): "Las transformaciones profundas son lentas y a veces dolorosas. Los temas de herencias, deudas y pérdidas requieren atención. Con tiempo desarrollas una fortaleza interior frente a lo inevitable.",
    ("Saturno", 9): "La expansión filosófica o académica requiere esfuerzo y tiempo. Pueden existir obstáculos para viajar o estudiar. Con tiempo te conviertes en un sabio de gran profundidad y rigor.",
    ("Saturno", 10): "Saturno en su casa natural: la carrera es la gran lección de vida. El éxito llega tarde pero es duradero. Tienes vocación de autoridad y debes ganarte el reconocimiento sin atajos.",
    ("Saturno", 11): "Las amistades son pocas pero profundas. Puede haber aislamiento o decepción con los grupos. Con tiempo encuentras una comunidad genuina basada en valores compartidos.",
    ("Saturno", 12): "Las limitaciones más profundas son interiores. Puede haber una carga de karma o responsabilidades invisibles. Con tiempo el retiro, la meditación y el servicio desinteresado son caminos de liberación.",

    # URANO en casas
    ("Urano", 1): "Personalidad excéntrica, independiente y difícil de encasillar. Los cambios en la identidad son frecuentes y sorpresivos.",
    ("Urano", 2): "Las finanzas son erráticas e impredecibles. Los ingresos pueden llegar de formas inesperadas.",
    ("Urano", 3): "Mente brillante, original y heterodoxa. Comunicación poco convencional. Los hermanos pueden ser excéntricos o muy diferentes.",
    ("Urano", 4): "El hogar puede ser inestable o poco convencional. Mudanzas frecuentes o familia atípica.",
    ("Urano", 5): "Creatividad revolucionaria. Los romances son inesperados e intensos. Los hijos pueden ser muy independientes.",
    ("Urano", 6): "El trabajo necesita libertad y variedad. Puede haber cambios frecuentes de empleo. La salud responde bien a enfoques alternativos.",
    ("Urano", 7): "Las relaciones son inesperadas y poco convencionales. Puede haber separaciones súbitas. La pareja suele ser muy independiente.",
    ("Urano", 8): "Los cambios más profundos llegan de forma inesperada. Herencias o pérdidas súbitas. Interés por lo oculto y lo científico a la vez.",
    ("Urano", 9): "Filosofía revolucionaria y viajes inesperados. Rechazo al dogma religioso. Mente abierta a ideas que rompen paradigmas.",
    ("Urano", 10): "La carrera es poco convencional y sujeta a cambios repentinos. Talento para innovar en el ámbito profesional.",
    ("Urano", 11): "Urano en casa propia: redes de personas originales e innovadoras. Las causas colectivas implican revolución real.",
    ("Urano", 12): "Los cambios más profundos ocurren en lo invisible. Intuición súbita y experiencias espirituales inesperadas.",

    # NEPTUNO en casas
    ("Neptuno", 1): "Personalidad elusiva, empática y difícil de definir. Tienes una presencia etérea y cambiante.",
    ("Neptuno", 2): "La relación con el dinero es confusa o idealizada. Pueden existir pérdidas por engaños o excesiva generosidad.",
    ("Neptuno", 3): "Pensamiento intuitivo, poético y no lineal. La comunicación puede ser imprecisa o muy artística.",
    ("Neptuno", 4): "El hogar tiene una dimensión espiritual o confusa. La memoria de la infancia puede ser nebulosa o idealizada.",
    ("Neptuno", 5): "Creatividad artística profunda. El amor tiene una dimensión romántica e idealizada.",
    ("Neptuno", 6): "El trabajo cotidiano tiene vocación de servicio. La salud puede ser delicada o difícil de diagnosticar.",
    ("Neptuno", 7): "La pareja puede ser idealizada o elusiva. Las relaciones tienen una dimensión espiritual o de sacrificio.",
    ("Neptuno", 8): "Lo místico y lo profundo se fusionan. Intuición excepcional para los misterios de la vida y la muerte.",
    ("Neptuno", 9): "Neptuno en casa propia: fe profunda y espiritualidad genuina. Los viajes pueden ser transformadores o confusos.",
    ("Neptuno", 10): "La carrera tiene vocación artística o de servicio invisible. La reputación puede ser nebulosa o glamurosa.",
    ("Neptuno", 11): "Los grupos pueden ser fuente de confusión o inspiración espiritual. Las esperanzas son grandes pero a veces poco realistas.",
    ("Neptuno", 12): "Neptuno en casa propia: vida interior muy rica. La espiritualidad y la soledad son fuentes de profunda renovación.",

    # PLUTÓN en casas
    ("Plutón", 1): "Presencia intensa y magnética. La identidad ha pasado por transformaciones radicales. Tienes una voluntad de hierro.",
    ("Plutón", 2): "El dinero y los recursos son fuentes de poder y transformación. Pueden existir pérdidas totales seguidas de recuperaciones completas.",
    ("Plutón", 3): "La mente es investigadora y penetrante. Las palabras pueden tener un poder transformador o destructivo.",
    ("Plutón", 4): "El hogar y la familia han sido escenario de transformaciones profundas. Las raíces contienen poder y sombra.",
    ("Plutón", 5): "La creatividad es transformadora e intensa. El amor tiene un componente obsesivo o regenerador.",
    ("Plutón", 6): "El trabajo implica transformación: medicina, investigación, psicología. La salud puede pasar por crisis profundas que forjan la fortaleza.",
    ("Plutón", 7): "Las relaciones son intensas y transformadoras. La pareja puede ser muy poderosa o controladora. Las asociaciones cambian la vida profundamente.",
    ("Plutón", 8): "Plutón en casa propia: máxima intensidad en los temas de la muerte, el sexo, el poder y la transformación. Extraordinaria capacidad de regeneración.",
    ("Plutón", 9): "La filosofía de vida pasa por crisis y renovaciones profundas. Los viajes pueden ser transformadores. Tendencia al fanatismo que debe vigilarse.",
    ("Plutón", 10): "La carrera implica poder y transformación. Puedes ser una figura de autoridad que polariza. El éxito viene acompañado de responsabilidades enormes.",
    ("Plutón", 11): "Los grupos y las causas colectivas implican dinámicas de poder. Las amistades se transforman radicalmente. Puedes ser un agente de cambio en las redes.",
    ("Plutón", 12): "El poder opera desde las sombras. La transformación más profunda es la interior. Tienes acceso a dimensiones del inconsciente poco comunes.",

    # NODO NORTE en casas
    ("Nodo Norte", 1): "Tu destino evolutivo es desarrollar la identidad propia, el coraje y la iniciativa individual frente a la dependencia del pasado.",
    ("Nodo Norte", 2): "Tu destino es construir seguridad material y emocional propia, desarrollando tus talentos y valores genuinos.",
    ("Nodo Norte", 3): "Tu destino es aprender a comunicar, conectar ideas y moverse con agilidad en el entorno cercano.",
    ("Nodo Norte", 4): "Tu destino es crear raíces, hogar y vida familiar profunda más allá del éxito externo.",
    ("Nodo Norte", 5): "Tu destino es la autoexpresión creativa, el amor genuino y la alegría de vivir con autenticidad.",
    ("Nodo Norte", 6): "Tu destino es el servicio concreto, la salud y el trabajo bien hecho como forma de contribución real.",
    ("Nodo Norte", 7): "Tu destino es aprender a relacionarte y comprometerse con el otro de forma madura y equilibrada.",
    ("Nodo Norte", 8): "Tu destino implica la transformación profunda, el manejo del poder y el aprendizaje de soltar lo que ya murió.",
    ("Nodo Norte", 9): "Tu destino es expandirte filosófica y geográficamente, desarrollando una fe y una visión del mundo propias.",
    ("Nodo Norte", 10): "Tu destino es alcanzar una posición visible y de autoridad en el mundo, asumiendo la responsabilidad pública.",
    ("Nodo Norte", 11): "Tu destino es la participación en grupos, causas colectivas y la construcción de un futuro mejor para todos.",
    ("Nodo Norte", 12): "Tu destino es la espiritualidad, el retiro interior y la compasión universal que va más allá del ego.",
}

# ─────────────────────────────────────────────────────────────────────────────
# ASPECTOS NOTABLES (pares específicos)
# ─────────────────────────────────────────────────────────────────────────────

NOTABLE_ASPECTS: dict[tuple[str, str, str], str] = {
    ("Sol", "Conjunción", "Luna"): "La voluntad y las emociones actúan en la misma dirección; hay coherencia interna pero puede haber dificultad para ver la perspectiva del otro. Naces cerca de la Luna Nueva.",
    ("Sol", "Oposición", "Luna"): "La voluntad y las emociones están en tensión permanente. Ves ambos lados de cada situación y puedes ser un mediador excepcional, pero internamente sientes que partes de ti van en direcciones opuestas. Naces cerca de la Luna Llena.",
    ("Sol", "Cuadratura", "Luna"): "Hay una tensión entre tu voluntad y tus necesidades emocionales que impulsa el crecimiento. Las decisiones importantes suelen implicar un costo emocional o la necesidad de renunciar a algo.",
    ("Sol", "Cuadratura", "Saturno"): "La autoconfianza se construye lentamente y con esfuerzo. Puedes sentir que el éxito llega con más trabas que a otros. Con el tiempo, la disciplina forjada por esta tensión produce logros de enorme solidez.",
    ("Sol", "Conjunción", "Saturno"): "Tu identidad está marcada por la responsabilidad, la seriedad y la disciplina. Puedes madurar muy rápido y cargar con más de lo que corresponde. El reconocimiento llega tarde pero es duradero.",
    ("Sol", "Trígono", "Saturno"): "La disciplina y la ambición fluyen de forma natural en tu personalidad. Tienes constancia y capacidad para construir con paciencia sin perder la confianza.",
    ("Sol", "Cuadratura", "Urano"): "Tu individualidad choca con las estructuras establecidas. Puedes vivir cambios abruptos en tu identidad o carrera. La rebeldía es parte de tu proceso de crecimiento.",
    ("Sol", "Conjunción", "Júpiter"): "Optimismo, expansión y una presencia generosa. La vida tiende a fluir con relativa facilidad. El riesgo es el exceso de confianza o la tendencia a prometer más de lo que puedes cumplir.",
    ("Luna", "Cuadratura", "Saturno"): "Las emociones están frenadas por el miedo, la autocrítica o la frialdad aprendida en la infancia. El proceso de liberación emocional es largo pero profundamente transformador.",
    ("Luna", "Conjunción", "Saturno"): "La vida emocional es seria, contenida y puede estar marcada por la melancolía. La madre o el entorno familiar fue exigente o frío. Con el tiempo desarrollas una fortaleza emocional real.",
    ("Luna", "Conjunción", "Neptuno"): "La vida emocional es muy porosa e intuitiva; puedes absorber los estados ajenos sin darte cuenta. Gran creatividad artística y espiritualidad. Cuidado con la idealización de las relaciones.",
    ("Luna", "Conjunción", "Plutón"): "Las emociones son intensas, transformadoras y a veces obsesivas. Las relaciones madre-hijo pueden haber sido de gran intensidad o control. Capacidad de regeneración emocional extraordinaria.",
    ("Mercurio", "Cuadratura", "Neptuno"): "La mente puede verse nublada por la confusión o la idealización. Gran creatividad e intuición pero dificultad para mantener los pies en el suelo intelectualmente.",
    ("Mercurio", "Conjunción", "Saturno"): "Mente seria, estructurada y de gran profundidad. El pensamiento es lento pero riguroso. Excelente para cualquier trabajo que requiera precisión y autoridad intelectual.",
    ("Venus", "Cuadratura", "Marte"): "La vida amorosa está llena de tensión entre el deseo y el afecto, entre la conquista y la armonía. Las relaciones son apasionadas pero pueden ser conflictivas. Gran atracción sexual.",
    ("Venus", "Conjunción", "Marte"): "La atracción física y el afecto se fusionan: eres una persona intensamente apasionada. El amor y la sexualidad están profundamente vinculados.",
    ("Venus", "Cuadratura", "Saturno"): "El amor llega con restricciones, demoras o lecciones difíciles. Puede haber miedo a la intimidad o relaciones con personas mayores o con cargas emocionales. Con el tiempo el amor se vuelve más maduro y duradero.",
    ("Venus", "Conjunción", "Júpiter"): "El amor y la abundancia van de la mano. Eres generoso, atractivo y atraes situaciones de expansión afectiva y material. El exceso puede ser el desafío.",
    ("Marte", "Cuadratura", "Saturno"): "La energía choca con los límites: puedes sentir frustración constante o que tus esfuerzos son frenados. Con el tiempo aprendes a actuar con estrategia y disciplina, lo que produce resultados extraordinarios.",
    ("Marte", "Conjunción", "Saturno"): "La energía es controlada y disciplinada. Puedes trabajar con una paciencia y resistencia notables. El riesgo es la represión de la rabia que puede volverse física.",
    ("Júpiter", "Cuadratura", "Saturno"): "Tensión entre la expansión y la restricción: avances y retrocesos, optimismo y pesimismo alternativos. Con el tiempo esta tensión genera una sabiduría equilibrada entre el sueño y la realidad.",
    ("Saturno", "Conjunción", "Plutón"): "Una generación marcada por la transformación de las estructuras de poder. En lo personal: una fuerza de voluntad extraordinaria forjada en la adversidad. Las crisis son el motor del crecimiento.",
    ("Saturno", "Cuadratura", "Plutón"): "Las transformaciones profundas chochan con las estructuras establecidas. Hay desafíos de poder y control que requieren un proceso de maduración largo y serio.",
}


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL DE ENSAMBLAJE
# ─────────────────────────────────────────────────────────────────────────────

def build_natal_planet_text(
    planet_name: str,
    sign: str,
    house: int,
    dignity: str,
    retrograde: bool,
    aspects: list,          # lista de objetos Aspect donde planet1 o planet2 == planet_name
) -> str:
    """Construye el texto de interpretación completo para un planeta en la carta natal."""
    parts = []

    # 1. Texto planeta en signo
    sign_text = PLANET_IN_SIGN.get((planet_name, sign))
    if sign_text:
        parts.append(sign_text)

    # 2. Texto planeta en casa
    house_text = PLANET_IN_HOUSE.get((planet_name, house))
    if house_text:
        parts.append(f"En la Casa {house}: {house_text}")

    # 3. Dignidad
    from core.interpretations import DIGNITY_DESCRIPTIONS
    dignity_desc = DIGNITY_DESCRIPTIONS.get(dignity, "")
    dig_note = f"Dignidad: {dignity}"
    if dignity_desc:
        dig_note += f" — {dignity_desc}"
    if retrograde:
        dig_note += ". Está retrógrado, lo que interioriza e intensifica su expresión."
    parts.append(dig_note)

    # 4. Aspectos relevantes del planeta
    asp_notes = []
    for asp in aspects:
        other = asp.planet2 if asp.planet1 == planet_name else asp.planet1
        key1 = (planet_name, asp.aspect_name, other)
        key2 = (other, asp.aspect_name, planet_name)
        nota = NOTABLE_ASPECTS.get(key1) or NOTABLE_ASPECTS.get(key2)
        if nota:
            asp_notes.append(f"{asp.aspect_name} con {other} (orbe {asp.orb}°): {nota}")
        else:
            asp_notes.append(f"{asp.aspect_name} con {other} (orbe {asp.orb}°)")
    if asp_notes:
        parts.append("Aspectos: " + " | ".join(asp_notes))

    return "\n\n".join(parts)


def build_asc_text(asc_sign: str) -> str:
    """Texto para el Ascendente."""
    return ASC_IN_SIGN.get(asc_sign, f"Ascendente en {asc_sign}.")
