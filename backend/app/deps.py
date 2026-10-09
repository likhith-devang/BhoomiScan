from collections.abc import Callable
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.constants import ALL_CASE_ACCESS_ROLES, DEFAULT_SIGNUP_ROLE, PDF_ROLES
from app.database import get_db
from app.models.user import User
from app.services.auth import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Please log in to continue.")

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = UUID(payload["sub"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Your session has expired. Please log in again.")

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Please log in to continue.")
    if not getattr(user, "role", None):
        user.role = DEFAULT_SIGNUP_ROLE
    return user


def require_roles(*allowed: str) -> Callable:
    allowed_set = set(allowed)

    def _checker(current_user: User = Depends(get_current_user)) -> User:
        role = getattr(current_user, "role", None) or ""
        if role not in allowed_set:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Your role is not allowed to perform this action.",
            )
        return current_user

    return _checker


def can_access_all_cases(user: User) -> bool:
    return getattr(user, "role", None) in ALL_CASE_ACCESS_ROLES


def can_generate_pdf(user: User) -> bool:
    return getattr(user, "role", None) in PDF_ROLES


def assert_case_access(user: User, case_owner_id: UUID) -> None:
    if can_access_all_cases(user):
        return
    if user.id != case_owner_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cannot open this property file.")
