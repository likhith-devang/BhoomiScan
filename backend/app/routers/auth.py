from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.constants import DEFAULT_SIGNUP_ROLE
from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserResponse
from app.services.audit_service import record_audit
from app.services.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)) -> User:
    existing = db.scalar(select(User).where(User.username == payload.username.strip()))
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already exists.")

    user = User(
        username=payload.username.strip(),
        password_hash=hash_password(payload.password),
        role=DEFAULT_SIGNUP_ROLE,
    )
    db.add(user)
    db.flush()
    record_audit(
        db,
        action="USER_SIGNUP",
        actor=user,
        resource_type="user",
        resource_id=user.id,
        detail="New buyer account created.",
    )
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.username == payload.username.strip()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid username or password.")
    record_audit(
        db,
        action="USER_LOGIN",
        actor=user,
        resource_type="user",
        resource_id=user.id,
        detail="Successful login.",
        commit=True,
    )
    role = getattr(user, "role", None) or DEFAULT_SIGNUP_ROLE
    return TokenResponse(access_token=create_access_token(user.id, user.username, role=role))


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
