from __future__ import annotations

import re
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.config import Settings
from app.constants import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, FILE_SIGNATURES

UNSAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_original_name(filename: str) -> str:
    name = Path(filename or "upload").name
    name = UNSAFE_CHARS.sub("_", name).strip("._") or "upload"
    return name[:180]


def _extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def sniff_kind(header: bytes, extension: str) -> str | None:
    signatures = FILE_SIGNATURES.get(extension)
    if not signatures:
        return None
    if any(header.startswith(sig) for sig in signatures):
        if extension == ".pdf":
            return "application/pdf"
        if extension == ".png":
            return "image/png"
        return "image/jpeg"
    return None


def validate_upload(file: UploadFile, raw: bytes, settings: Settings) -> tuple[str, str]:
    if not raw:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This file is empty.")

    if len(raw) > settings.max_file_size_bytes:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"This file is too big. The limit is {settings.MAX_FILE_SIZE_MB} MB.",
        )

    original = _safe_original_name(file.filename or "upload")
    extension = _extension(original)
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Please upload a PDF, PNG, JPG, or JPEG file.",
        )

    declared = (file.content_type or "").split(";")[0].strip().lower()
    if declared and declared not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Please upload a PDF, PNG, JPG, or JPEG file.",
        )

    sniffed = sniff_kind(raw[:16], extension)
    if not sniffed:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "This file is not a valid PDF, PNG, or JPG.",
        )

    return original, sniffed


def store_document(property_case_id: uuid.UUID, original_filename: str, raw: bytes, settings: Settings) -> tuple[str, Path]:
    case_dir = settings.STORAGE_DIR / str(property_case_id)
    case_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}_{_safe_original_name(original_filename)}"
    dest = case_dir / stored_name
    dest.write_bytes(raw)
    return stored_name, dest
