from __future__ import annotations

import io
import logging
import time
import zipfile
from pathlib import Path

import requests

from app.config import get_settings
from app.constants import ENGLISH_LANGUAGE, KANNADA_LANGUAGE, SARVAM_TERMINAL_STATUSES, TRANSLATE_CHUNK_SIZE

logger = logging.getLogger(__name__)


class SarvamError(RuntimeError):
    """Raised when Sarvam Document AI cannot complete a step."""


def _client():
    settings = get_settings()
    key = (settings.SARVAM_API_KEY or "").strip()
    if not key:
        raise SarvamError("Sarvam API key is not configured. Add SARVAM_API_KEY to your .env file.")
    try:
        from sarvamai import SarvamAI
    except ImportError as exc:
        raise SarvamError("The Sarvam SDK is not installed. Run: pip install sarvamai") from exc
    return SarvamAI(api_subscription_key=key)


def _poll_job(client, job_id: str):
    settings = get_settings()
    deadline = time.time() + settings.SARVAM_MAX_WAIT_SECONDS
    last = None
    while time.time() < deadline:
        last = client.doc_ai.get_status(job_id=job_id)
        status_name = str(getattr(last, "status", "") or "").lower()
        if status_name in SARVAM_TERMINAL_STATUSES:
            return last
        time.sleep(settings.SARVAM_POLL_SECONDS)
    raise SarvamError("Document reading timed out. Please try again.")


def _job_id(job) -> str:
    value = getattr(job, "job_id", None) or getattr(job, "id", None)
    if not value:
        raise SarvamError("Sarvam did not return a job id.")
    return str(value)


def _clean_text(value: str | None) -> str:
    return (value or "").replace("\x00", "").strip()


def _text_from_digitise_results(results) -> str:
    dumped = results.model_dump() if hasattr(results, "model_dump") else results
    if not isinstance(dumped, dict):
        return ""
    lines: list[str] = []
    for document in dumped.get("documents") or []:
        for page in document.get("pages") or []:
            page_no = page.get("page_num") or page.get("page_number")
            page_bits: list[str] = []
            if page.get("content"):
                page_bits.append(str(page["content"]))
            for block in page.get("blocks") or []:
                text = _clean_text(block.get("text") if isinstance(block, dict) else "")
                if text:
                    page_bits.append(text)
            body = "\n".join(page_bits).strip()
            if body:
                prefix = f"[Page {page_no}]\n" if page_no else ""
                lines.append(prefix + body)
    return _clean_text("\n\n".join(lines))


def _text_from_zip(content: bytes) -> str:
    parts: list[str] = []
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        for name in archive.namelist():
            lowered = name.lower()
            if not lowered.endswith((".md", ".html", ".htm", ".txt", ".json")):
                continue
            parts.append(archive.read(name).decode("utf-8", errors="replace"))
    return _clean_text("\n\n".join(parts))


def _download_output_text(url: str) -> str:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    payload = response.content or b""
    if payload[:2] == b"PK":
        return _text_from_zip(payload)
    return _clean_text(payload.decode("utf-8", errors="replace"))


def digitise_document(file_path: str, filename: str, mime_type: str, language: str = KANNADA_LANGUAGE) -> str:
    path = Path(file_path)
    if not path.exists():
        raise SarvamError("The uploaded file could not be found on the server.")
    try:
        client = _client()
        raw = path.read_bytes()
        job = client.doc_ai.digitise(
            file=[(filename, io.BytesIO(raw), mime_type)],
            language=language,
            output_format="md",
        )
        status = _poll_job(client, _job_id(job))
        status_name = str(getattr(status, "status", "") or "").lower()
        if status_name in {"failed", "rejected"}:
            raise SarvamError("Sarvam could not read this document.")
        text = ""
        try:
            results = client.doc_ai.get_results(job_id=_job_id(job))
            text = _text_from_digitise_results(results)
        except Exception:
            logger.exception("Sarvam get_results failed; trying download URL.")
        if not text:
            download = client.doc_ai.get_download_url(job_id=_job_id(job))
            url = getattr(download, "url", None)
            if url:
                text = _download_output_text(url)
        if not text:
            raise SarvamError("We could not read any text from this document.")
        return text
    except SarvamError:
        raise
    except Exception as exc:
        logger.exception("Sarvam digitise failed.")
        raise SarvamError("Sarvam could not read this document.") from exc


def extract_fields(file_path: str, filename: str, mime_type: str, schema: dict) -> dict:
    import json

    path = Path(file_path)
    try:
        client = _client()
        raw = path.read_bytes()
        job = client.doc_ai.extract(
            file=[(filename, io.BytesIO(raw), mime_type)],
            schema=json.dumps(schema),
            output_format="json",
        )
        status = _poll_job(client, _job_id(job))
        status_name = str(getattr(status, "status", "") or "").lower()
        if status_name in {"failed", "rejected"}:
            return {}
        results = client.doc_ai.get_results(job_id=_job_id(job))
    except Exception:
        logger.exception("Sarvam extract failed; continuing with source-text fallback.")
        return {}
    if isinstance(results, dict):
        return results
    dumped = results.model_dump() if hasattr(results, "model_dump") else {}
    if not isinstance(dumped, dict):
        return {}
    for key in ("data", "result", "fields", "extracted"):
        value = dumped.get(key)
        if isinstance(value, dict):
            return value
    return dumped if any(k in dumped for k in ("property", "ownership", "litigation")) else {}


def translate_text(text: str, source_language: str = KANNADA_LANGUAGE, target_language: str = ENGLISH_LANGUAGE) -> str:
    if not text.strip():
        return ""
    try:
        client = _client()
        chunks = [text[i : i + TRANSLATE_CHUNK_SIZE] for i in range(0, len(text), TRANSLATE_CHUNK_SIZE)]
        parts: list[str] = []
        for chunk in chunks:
            result = client.text.translate(
                input=chunk,
                source_language_code=source_language,
                target_language_code=target_language,
                model="sarvam-translate:v1",
            )
            translated = (
                getattr(result, "translated_text", None)
                or getattr(result, "output", None)
                or (result.get("translated_text") if isinstance(result, dict) else None)
            )
            parts.append(str(translated or chunk))
        return _clean_text("\n".join(parts))
    except Exception as exc:
        logger.exception("Sarvam translate failed.")
        raise SarvamError("The document was read, but English translation failed. Please try again.") from exc
