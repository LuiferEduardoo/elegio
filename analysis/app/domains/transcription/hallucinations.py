"""Filter known Whisper hallucinations from transcript segments.

When Whisper runs on long stretches of silence, music, or background noise,
it sometimes emits phantom Spanish text it learned from training data —
overwhelmingly the subtitle-credits tagline ``Subtítulos realizados por la
comunidad de Amara.org`` (it appears at the end of countless YouTube
videos) and a handful of "gracias por ver" variants. We also drop runs of
consecutive duplicated text, the other reliable signature of Whisper looping
on silence. Real speech almost never produces either pattern.

The cached ``transcript.json`` keeps the raw Whisper output for auditing;
filtering happens in memory on the way to the aligner.
"""

import unicodedata

from app.domains.transcription.whisper_client import TranscriptSegment

KNOWN_PHRASES: frozenset[str] = frozenset(
    {
        "subtitulos realizados por la comunidad de amara.org",
        "subtitulos por la comunidad de amara.org",
        "subtitulos creados por la comunidad de amara.org",
        "subtitulado por la comunidad de amara.org",
        "subtitulos realizados por subadictos.net",
        "subtitulos por aitor garcia ruiz",
        "muchas gracias por ver el video",
        "gracias por ver el video",
        "gracias por ver este video",
        "gracias por ver mi video",
    }
)


def _normalize(text: str) -> str:
    """Lowercase, strip diacritics, and trim surrounding punctuation/whitespace."""
    no_accents = "".join(
        c for c in unicodedata.normalize("NFKD", text) if unicodedata.category(c) != "Mn"
    )
    return no_accents.lower().strip().strip(".,!?¡¿;:\"' ")


def is_known_hallucination(text: str) -> bool:
    return _normalize(text) in KNOWN_PHRASES


def filter_hallucinations(segments: list[TranscriptSegment]) -> list[TranscriptSegment]:
    out: list[TranscriptSegment] = []
    last_norm: str | None = None
    for seg in segments:
        norm = _normalize(seg.text)
        if not norm or norm in KNOWN_PHRASES:
            continue
        if norm == last_norm:
            # Drop consecutive duplicates (typical hallucination on silence).
            continue
        last_norm = norm
        out.append(seg)
    return out
