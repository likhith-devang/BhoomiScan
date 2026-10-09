from __future__ import annotations

import re

from app.constants import DOCUMENT_TYPES, ENGLISH_LANGUAGE, KANNADA_LANGUAGE

PROPERTY_CUES = (
    "sale deed",
    "encumbrance",
    "khata",
    "katha",
    "survey",
    "sy. no",
    "sy no",
    "property",
    "mortgage",
    "mutation",
    "registration",
    "vendor",
    "vendee",
    "buyer",
    "seller",
    "schedule",
    "square",
    "sq ft",
    "sq.ft",
    "village",
    "taluk",
    "district",
    "ಕ್ರಯ",
    "ಮಾರಾಟ",
    "ಸರ್ವೆ",
    "ಖಾತಾ",
)

NON_PROPERTY_CUES = (
    "resume",
    "curriculum vitae",
    "invoice only",
    "medical report",
    "prescription",
    "marksheet",
    "driving licence",
    "passport application",
)


def is_property_document(document_type: str | None, text: str, filename: str = "") -> tuple[bool, str]:
    """AI analysis is restricted to property-related papers only."""
    dtype = (document_type or "OTHER").upper()
    haystack = f"{filename}\n{text or ''}".lower()
    if dtype in DOCUMENT_TYPES and dtype != "OTHER":
        return True, "Classified as a property document."
    if any(cue in haystack for cue in NON_PROPERTY_CUES) and not any(cue in haystack for cue in PROPERTY_CUES):
        return False, "This file does not look like a property document. AI analysis is limited to property papers."
    if any(cue in haystack for cue in PROPERTY_CUES):
        return True, "Property keywords found in the document."
    return False, "AI analysis is restricted to property documents such as sale deeds, EC, khata, and related papers."


def validate_english_working_text(
    text: str,
    detected_language: str,
    *,
    classified_property_type: bool = False,
) -> dict:
    """Validate English (or translated) working text before rules run."""
    source = text or ""
    latin = len(re.findall(r"[A-Za-z]", source))
    kannada = len(re.findall(r"[\u0C80-\u0CFF]", source))
    words = re.findall(r"[A-Za-z]{3,}", source)
    unique_ratio = (len(set(w.lower() for w in words)) / len(words)) if words else 0.0
    ok = True
    notes: list[str] = []
    # Short sketches / certificates may have few Latin letters; allow them once classified.
    min_latin = 20 if classified_property_type else 40
    if detected_language == ENGLISH_LANGUAGE:
        if latin < min_latin:
            ok = False
            notes.append("English document has too little readable Latin text for validation.")
        elif latin < 40 and classified_property_type:
            notes.append("English property document validated (short form); translation skipped.")
        else:
            notes.append("English document validated; translation skipped.")
    elif detected_language == KANNADA_LANGUAGE:
        if latin < 30 and kannada > 0:
            notes.append("Kannada page translated, but English working text is thin; rules may be limited.")
        else:
            notes.append("Kannada content translated to English for rule evaluation.")
    if words and unique_ratio < 0.15 and len(words) > 40:
        ok = False
        notes.append("Working text looks repetitive or low-quality; re-upload a clearer scan.")
    return {
        "ok": ok,
        "latin_chars": latin,
        "kannada_chars": kannada,
        "unique_word_ratio": round(unique_ratio, 3),
        "notes": notes,
    }
