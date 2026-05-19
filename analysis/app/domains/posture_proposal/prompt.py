from app.domains.posture_proposal.rubrics import RUBRICS

def build_prompt(category_slug: str, category_name: str, proposal_text: str) -> str:
    if category_slug not in RUBRICS:
        raise ValueError(
            f"No rubric defined for category '{category_slug}'. "
            f"Available: {list(RUBRICS.keys())}"
        )

    rubric = RUBRICS[category_slug]
    pn = rubric["polo_negativo"]
    pp = rubric["polo_positivo"]

    anchors_str = "\n".join(
        f"  {value:+.2f}: {desc}"
        for value, desc in sorted(rubric["anclajes"].items())
    )

    return f"""Actúa como un experto en Ciencia Política comparada y análisis de políticas públicas. Vas a clasificar el contenido de una propuesta política en un eje descriptivo. Tu tarea es taxonómica, no evaluativa: no juzgas si la propuesta es buena o mala, solo dónde se ubica entre dos enfoques legítimos. Los signos -1 y +1 son posiciones numéricas en una recta, no juicios de valor.

    EJE: {category_name}

    Extremo -1.0 — enfoque "{pn['nombre']}": {pn['descripcion']}
    Extremo +1.0 — enfoque "{pp['nombre']}": {pp['descripcion']}

    ANCLAJES (referencias para ubicar la propuesta):
    {anchors_str}

    PROPUESTA:
    \"\"\"
    {proposal_text}
    \"\"\"

    PASO 1 — RELEVANCIA (obligatorio antes de puntuar):
    Antes de asignar un score, determina si la propuesta aborda este eje. Marca `addresses_axis`:
    - "direct": la propuesta habla explícitamente del tema del eje.
    - "tangential": la propuesta menciona el tema solo de pasada o como medio para otro fin.
    - "none": la propuesta NO aborda este eje en absoluto (ej. una propuesta sobre vivienda evaluada en un eje de política exterior).

    Si `addresses_axis = "none"`, devuelve `score: null` y `confidence: "not_applicable"`. NO fuerces un 0. Un 0 significa "la propuesta toma una posición central o equilibrada en este eje", no "la propuesta no habla del eje".

    PASO 2 — UBICACIÓN EN EL EJE (solo si addresses_axis ≠ "none"):

    Reserva el score 0.0 EXCLUSIVAMENTE para uno de estos dos casos:
    (a) CENTRO GENUINO: la propuesta combina explícitamente elementos de ambos polos con peso similar, o adopta una postura de equilibrio deliberado (ej. "modelo mixto", "combinar X e Y"). En este caso la confianza puede ser MEDIUM o HIGH.
    (b) AMBIGÜEDAD REAL sobre el eje: la propuesta toca el tema pero usa lenguaje tan genérico que podría justificar cualquier polo. Confianza LOW.

    Si la propuesta aborda el eje y se inclina aunque sea débilmente hacia un polo, NO uses 0. Usa ±0.25 (inclinación leve), ±0.5 (inclinación moderada), ±0.75 (posición clara), o ±1.0 (posición explícita y categórica).

    Señales que justifican alejarse de 0 incluso con poca información:
    - Vocabulario asociado a un polo (ej. "soberanía", "libre empresa", "comunidades", "mercado").
    - Adopción de marcos conceptuales propios de un enfoque.
    - Crítica o rechazo explícito al otro polo.
    - Inclusión de medidas características de un polo aunque sin detallar mecanismos.

    NIVELES DE CONFIANZA:
    - high: posición explícita y específica, O centro genuino con elementos balanceados.
    - medium: posición inferible del lenguaje, marcos o medidas mencionadas.
    - low: el texto es genuinamente ambiguo entre dos lecturas plausibles. NO uses LOW como sinónimo de "el texto es corto" si las señales lingüísticas son claras.

    REGLAS ANTI-SESGO:
    - No marques LOW solo porque la propuesta es breve; brevedad no equivale a ambigüedad.
    - Si dudas entre 0 y ±0.25, elige ±0.25: la inclinación débil es más informativa que el centro forzado.
    - "No menciona X mecanismo" no implica neutralidad si el lenguaje general apunta a un polo.
    - Distingue: ¿la propuesta es vaga sobre CÓMO implementar (mecanismos), o vaga sobre QUÉ enfoque adoptar (filosofía)? Solo lo segundo justifica acercarse a 0.

    PASO 3 — RAZONAMIENTO:
    Razona paso a paso. Cita fragmentos textuales que sustenten tu lectura. No infieras posiciones que el texto no sustente, pero tampoco descartes señales lingüísticas sutiles.

    Responde en JSON con los campos exactamente en este orden:
    addresses_axis, ambiguities, reasoning, confidence, score
    """