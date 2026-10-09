import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.constants import (
    ROLE_ADMIN,
    ROLE_ASSIGN_ROLES,
    ROLE_BUYER,
    ROLE_SECONDARY_ADMIN,
    ROLE_SUPER_ADMIN,
)
from app.database import get_db
from app.deps import require_roles
from app.models.audit import AuditLog
from app.models.user import User
from app.schemas.auth import AuditLogResponse, RoleUpdateRequest, UserResponse
from app.services.audit_service import record_audit

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(*ROLE_ASSIGN_ROLES)),
) -> list[User]:
    return list(db.scalars(select(User).order_by(User.created_at.desc())).all())


@router.patch("/users/{user_id}/role", response_model=UserResponse)
def assign_role(
    user_id: uuid.UUID,
    payload: RoleUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(*ROLE_ASSIGN_ROLES)),
) -> User:
    target = db.get(User, user_id)
    if target is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")

    new_role = payload.role
    actor_role = current_user.role

    if actor_role == ROLE_ADMIN:
        if new_role not in {ROLE_BUYER, ROLE_SECONDARY_ADMIN}:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Administrators may only assign Buyer or Secondary Admin roles.",
            )
        if target.role in {ROLE_SUPER_ADMIN, ROLE_ADMIN} and target.id != current_user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Administrators cannot change other admin roles.")

    if new_role == ROLE_SUPER_ADMIN and actor_role != ROLE_SUPER_ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only a Super Admin can grant Super Admin.")

    previous = target.role
    target.role = new_role
    db.add(target)
    record_audit(
        db,
        action="ROLE_ASSIGNED",
        actor=current_user,
        resource_type="user",
        resource_id=target.id,
        detail=f"Role changed from {previous} to {new_role}.",
        meta={"previous_role": previous, "new_role": new_role},
    )
    db.commit()
    db.refresh(target)
    return target


@router.get("/audit-logs", response_model=list[AuditLogResponse])
def list_audit_logs(
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(ROLE_SUPER_ADMIN, ROLE_ADMIN)),
) -> list[AuditLog]:
    return list(
        db.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)).all()
    )
