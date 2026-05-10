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

    return f"""Actúa como un experto en Ciencia Política comparada y análisis de políticas públicas.\
Vas a clasificar el contenido de una propuesta política en un eje \
descriptivo. Tu tarea es taxonómica, no evaluativa: no juzgas si la \
propuesta es buena o mala, solo dónde se ubica entre dos enfoques \
legítimos. Los signos -1 y +1 son posiciones numéricas en una recta, \
no juicios de valor.

EJE: {category_name}

Extremo -1.0 — enfoque "{pn['nombre']}": {pn['descripcion']}
Extremo +1.0 — enfoque "{pp['nombre']}": {pp['descripcion']}

ANCLAJES (referencias para ubicar la propuesta):
{anchors_str}

DISTRIBUCIÓN ESPERADA:
La mayoría de propuestas reales se ubican entre -0.5 y +0.5. Los \
valores extremos (-1.0, +1.0) requieren posiciones explícitas y \
específicas hacia uno de los enfoques. Si la propuesta es vaga, mixta \
o no aborda directamente el eje, el score debe estar cerca de 0 con \
confianza baja.

NIVELES DE CONFIANZA:
- high: la propuesta es explícita y específica sobre este eje.
- medium: la posición se infiere razonablemente del texto.
- low: el texto es vago, ambiguo, o solo toca el eje tangencialmente.

PROPUESTA:
\"\"\"
{proposal_text}
\"\"\"

INSTRUCCIONES:
- Razona paso a paso antes de calificar.
- No infieras posiciones que el texto no sustente.
- Usa incrementos de 0.25 para el score.

Responde en JSON con los campos exactamente en este orden: ambiguities, \
reasoning, confidence, score.
"""