from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.user import User


def record_audit(
    db: Session,
    *,
    action: str,
    actor: User | None = None,
    resource_type: str | None = None,
    resource_id: str | UUID | None = None,
    detail: str | None = None,
    meta: dict[str, Any] | None = None,
    commit: bool = False,
) -> AuditLog:
    row = AuditLog(
        actor_user_id=actor.id if actor else None,
        actor_username=actor.username if actor else None,
        actor_role=getattr(actor, "role", None) if actor else None,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id is not None else None,
        detail=detail,
        meta=meta,
    )
    db.add(row)
    if commit:
        db.commit()
        db.refresh(row)
    else:
        db.flush()
    return row
