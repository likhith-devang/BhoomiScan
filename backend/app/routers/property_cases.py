import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.config import get_settings
from app.constants import CASE_STATUS_ACTIVE, DOCUMENT_STATUS_UPLOADED
from app.database import get_db
from app.deps import assert_case_access, can_access_all_cases, get_current_user
from app.models.document import Document
from app.models.property_case import PropertyCase
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.schemas.property_case import PropertyCaseCreate, PropertyCaseResponse, validate_domain_and_type
from app.services.audit_service import record_audit
from app.services.storage import store_document, validate_upload

router = APIRouter(prefix="/property-cases", tags=["property-cases"])


def _to_case_response(case: PropertyCase, document_count: int | None = None) -> PropertyCaseResponse:
    count = document_count if document_count is not None else len(case.documents or [])
    return PropertyCaseResponse(
        id=case.id,
        user_id=case.user_id,
        domain=case.domain,
        property_type=case.property_type,
        status=case.status,
        document_count=count,
        created_at=case.created_at,
        updated_at=case.updated_at,
    )


def _accessible_case(db: Session, case_id: uuid.UUID, user: User) -> PropertyCase:
    case = db.scalar(
        select(PropertyCase)
        .options(selectinload(PropertyCase.documents))
        .where(PropertyCase.id == case_id)
    )
    if case is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "We could not find this property file.")
    assert_case_access(user, case.user_id)
    return case


@router.post("", response_model=PropertyCaseResponse, status_code=status.HTTP_201_CREATED)
def create_property_case(
    payload: PropertyCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PropertyCaseResponse:
    try:
        domain, property_type = validate_domain_and_type(payload.domain, payload.property_type)
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc

    case = PropertyCase(
        user_id=current_user.id,
        domain=domain,
        property_type=property_type,
        status=CASE_STATUS_ACTIVE,
    )
    db.add(case)
    db.flush()
    record_audit(
        db,
        action="CASE_CREATED",
        actor=current_user,
        resource_type="property_case",
        resource_id=case.id,
        detail=f"Property case created ({domain}/{property_type}).",
    )
    db.commit()
    db.refresh(case)
    return _to_case_response(case, 0)


@router.get("", response_model=list[PropertyCaseResponse])
def list_property_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PropertyCaseResponse]:
    document_count = (
        select(func.count(Document.id))
        .where(Document.property_case_id == PropertyCase.id)
        .correlate(PropertyCase)
        .scalar_subquery()
    )
    query = select(PropertyCase, document_count).order_by(PropertyCase.created_at.desc())
    if not can_access_all_cases(current_user):
        query = query.where(PropertyCase.user_id == current_user.id)
    rows = db.execute(query).all()
    return [_to_case_response(case, count or 0) for case, count in rows]


@router.get("/{case_id}", response_model=PropertyCaseResponse)
def get_property_case(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PropertyCaseResponse:
    case = _accessible_case(db, case_id, current_user)
    return _to_case_response(case)


@router.post("/{case_id}/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    case_id: uuid.UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Document:
    case = _accessible_case(db, case_id, current_user)
    settings = get_settings()
    raw = await file.read()
    original_filename, file_type = validate_upload(file, raw, settings)
    stored_filename, dest = store_document(case.id, original_filename, raw, settings)

    document = Document(
        property_case_id=case.id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=str(dest),
        file_type=file_type,
        file_size=len(raw),
        status=DOCUMENT_STATUS_UPLOADED,
    )
    db.add(document)
    db.flush()
    record_audit(
        db,
        action="DOCUMENT_UPLOADED",
        actor=current_user,
        resource_type="document",
        resource_id=document.id,
        detail=f"Uploaded {original_filename}.",
        meta={"case_id": str(case.id)},
    )
    db.commit()
    db.refresh(document)
    return document


@router.get("/{case_id}/documents", response_model=list[DocumentResponse])
def list_documents(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Document]:
    case = _accessible_case(db, case_id, current_user)
    return sorted(case.documents, key=lambda item: item.created_at or item.id, reverse=True)


@router.delete("/{case_id}/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    case_id: uuid.UUID,
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    case = _accessible_case(db, case_id, current_user)
    document = next((item for item in case.documents if item.id == document_id), None)
    if document is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "We could not find this document.")
    stored = Path(document.file_path) if document.file_path else None
    record_audit(
        db,
        action="DOCUMENT_DELETED",
        actor=current_user,
        resource_type="document",
        resource_id=document.id,
        detail=f"Deleted {document.original_filename}.",
        meta={"case_id": str(case.id)},
    )
    db.delete(document)
    db.commit()
    if stored and stored.exists() and stored.is_file():
        stored.unlink()
