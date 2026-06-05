"""Cleanup heuristics for the raw text returned by trafilatura.

Trafilatura already strips ads, sidebars, and the page chrome, but the body
text it returns can still carry:
  - encoding garbage (mojibake from sites that double-encoded UTF-8 or served
    pages with the wrong charset),
  - stray URLs that survived the link-removal pass (image captions, social
    share blurbs, footer references),
  - newlines, tabs, and repeated spaces inherited from the source HTML.

This module is applied in :func:`app.domains.news.service.process_article`
so the JSON the pipeline emits is always one well-encoded, single-spaced
paragraph per article.
"""

import re

import ftfy

# http(s)://… or www.…  — broad enough to catch trailing URLs in captions
# without nuking surrounding punctuation.
_URL_RE = re.compile(r"https?://\S+|www\.\S+")

_WHITESPACE_RE = re.compile(r"\s+")

# Recurring publisher boilerplate that carries no article value: subscribe
# prompts, fact-check bot intros, network/credentials outros, etc. These repeat
# verbatim across many articles from the same outlet, so we strip them here
# instead of editing each JSON by hand (manual edits are lost when the pipeline
# re-aggregates). Add new phrases as you spot them; matching is whitespace- and
# case-insensitive and runs on the collapsed single-line text.
#
# Each entry anchors on a stable start and end phrase with a lazy ``.*?`` in
# between so wording drift inside the block doesn't break the match.
_BOILERPLATE_PATTERNS: list[str] = [
    # La Silla Vacía — Detector de Mentiras intro
    r"Escríbanos al DetectBot.*?la verificará para usted\.?",
    # La Silla Vacía — IFCN membership outro
    r"La Silla Vacía es parte del International Fact-Checking Network.*?"
    r"que pueden conocer acá\.?",
]
_BOILERPLATE_RE = re.compile("|".join(_BOILERPLATE_PATTERNS), re.IGNORECASE)

# Inline reference markers like "(1, 2)", "(1, 2, 3)", "(1, 2 y 3)" that some
# outlets append to sentences to cite their sources. We only strip lists of two
# or more numbers (comma- or "y"-separated) so a lone "(2023)" year is never
# touched. The leading space is consumed so "afirmación (1, 2)." → "afirmación.".
_REF_LIST_RE = re.compile(r"\s*\(\s*\d+(?:\s*(?:,|y|Y)\s*\d+)+\s*\)")

# Embedded tweet/X footers that leak into article text, e.g.
#   "… pic.twitter.com/XXXX — Revista Semana (@RevistaSemana) June 4, 2026 - …"
# Strip the image shortlink and the attribution (account + handle + date),
# including a trailing separator dash. Run BEFORE _HANDLE_RE since the date
# anchors the attribution match.
_TWEET_RE = re.compile(
    r"\s*pic\.twitter\.com/\S+"
    r"|\s*—\s*[^—]{0,60}?\(@\w+\)\s+[A-Za-z]+\s+\d{1,2}(?:,?\s*\d{4})?(?:\s*[-–])?"
)

# Standalone X/Twitter handles mentioned inline in prose, e.g.
# "Marco Rubio (@SecRubio), aseguró…" → "Marco Rubio, aseguró…". A parenthetical
# handle never carries the sentence, so dropping it is always safe.
_HANDLE_RE = re.compile(r"\s*\(@\w+\)")


def clean_content(text: str | None) -> str:
    """Fix encoding, strip URLs/boilerplate/tweets/refs, collapse whitespace."""
    if not text:
        return ""
    fixed = ftfy.fix_text(text)
    no_urls = _URL_RE.sub(" ", fixed)
    collapsed = _WHITESPACE_RE.sub(" ", no_urls).strip()
    no_boilerplate = _BOILERPLATE_RE.sub(" ", collapsed)
    no_tweets = _TWEET_RE.sub(" ", no_boilerplate)
    no_handles = _HANDLE_RE.sub("", no_tweets)
    no_refs = _REF_LIST_RE.sub("", no_handles)
    return _WHITESPACE_RE.sub(" ", no_refs).strip()


def clean_title(text: str | None) -> str | None:
    """Same fixes as :func:`clean_content` but preserves ``None`` for missing titles."""
    if text is None:
        return None
    cleaned = clean_content(text)
    return cleaned or None
