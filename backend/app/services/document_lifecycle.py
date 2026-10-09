from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from app.constants import DOCUMENT_STATUS_DISCARDED
from app.models.document import Document
from app.models.property_case import PropertyCase
from app.models.user import User
from app.services.audit_service import record_audit


def discard_case_documents(db: Session, case: PropertyCase, actor: User | None = None) -> int:
    """Delete uploaded bytes and scrub OCR text after a final report is generated."""
    discarded = 0
    for document in list(case.documents or []):
        path = Path(document.file_path) if document.file_path else None
        if path and path.exists() and path.is_file():
            path.unlink()
            discarded += 1
            parent = path.parent
            if parent.exists() and parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
        # Keep extracted_data for case recalculation / later report versions.
        # Remove OCR source text and the uploaded binary so personal papers are not retained.
        document.original_text = None
        document.translated_text = None
        document.processing_error = None
        document.status = DOCUMENT_STATUS_DISCARDED
        document.file_path = ""
        db.add(document)
    record_audit(
        db,
        action="DOCUMENTS_DISCARDED",
        actor=actor,
        resource_type="property_case",
        resource_id=case.id,
        detail=f"Discarded {discarded} uploaded file(s) after final report generation.",
        meta={"files_removed": discarded, "document_count": len(case.documents or [])},
    )
    return discarded
