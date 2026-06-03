"""Map anonymous pyannote labels (``SPEAKER_00``, ...) to real participant
names by asking Gemini to read a sample of utterances per speaker.

Strategy: collect the first N text snippets for each speaker label, send them
to Gemini along with the list of known participants, and ask for a strict
``{ "SPEAKER_00": "Name", ... }`` JSON mapping. Any speaker we cannot resolve
keeps its original label.
"""

import json
from collections import defaultdict

from google import genai
from google.genai import types

from app.config import settings
from app.domains.transcription.aligner import AlignedSegment

SAMPLE_PER_SPEAKER = 6
MAX_CHARS_PER_SAMPLE = 240
MODEL = "gemini-2.5-flash"

_PROMPT = """Sos un asistente que asigna nombres reales a etiquetas anónimas de diarización en una entrevista o debate político en español.

Participantes posibles (usá EXACTAMENTE estos nombres):
{participants}

Para cada etiqueta anónima, te paso una muestra de cosas que dijo. Devolvé un JSON plano `{{ "SPEAKER_00": "Nombre real", ... }}` mapeando cada etiqueta a uno de los participantes.

Reglas:
- Usá las pistas contextuales: presentaciones, preguntas vs respuestas, menciones por nombre, formalidad ("candidato, ¿usted...?").
- Si dos etiquetas claramente son la misma persona dividida por ruido, podés asignarles el mismo nombre.
- Si genuinamente no podés decidir, devolvé "Desconocido".
- Respondé SOLO el JSON, sin texto adicional.

Muestras:
{samples}
"""


def _collect_samples(aligned: list[AlignedSegment]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = defaultdict(list)
    for seg in aligned:
        if len(buckets[seg.speaker]) >= SAMPLE_PER_SPEAKER:
            continue
        snippet = seg.text.strip()
        if len(snippet) > MAX_CHARS_PER_SAMPLE:
            snippet = snippet[: MAX_CHARS_PER_SAMPLE - 1].rstrip() + "…"
        buckets[seg.speaker].append(snippet)
    return buckets


def _format_samples(buckets: dict[str, list[str]]) -> str:
    lines: list[str] = []
    for label in sorted(buckets):
        lines.append(f"[{label}]")
        for s in buckets[label]:
            lines.append(f"- {s}")
        lines.append("")
    return "\n".join(lines).rstrip()


def resolve_speaker_names(
    aligned: list[AlignedSegment], participants: list[str]
) -> dict[str, str]:
    """Return ``{ "SPEAKER_00": "Real Name", ... }``. Labels we cannot map are
    omitted (the caller should keep the original label for those)."""
    if not aligned or not participants:
        return {}

    buckets = _collect_samples(aligned)
    if not buckets:
        return {}

    prompt = _PROMPT.format(
        participants="\n".join(f"- {p}" for p in participants),
        samples=_format_samples(buckets),
    )

    client = genai.Client(api_key=settings.gemini_api_key)
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1,
        ),
    )
    raw = response.text or "{}"
    try:
        mapping = json.loads(raw)
    except json.JSONDecodeError:
        return {}

    cleaned: dict[str, str] = {}
    for label, name in mapping.items():
        if not isinstance(name, str):
            continue
        name = name.strip()
        if not name:
            continue
        if name in participants:
            cleaned[label] = name
        elif name.lower() == "desconocido":
            continue
    return cleaned
