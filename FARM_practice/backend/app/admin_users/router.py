from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from .schema import ReadAdminUser, CreateAdminUser, UpdateAdminUser
from .model import AdminUser
from .security import hash_password
from app.core.db import get_session

router = APIRouter(prefix="/admin_user", tags=["admin_user"])


@router.post("/", response_model=ReadAdminUser)
def create_admin_user(payload: CreateAdminUser, session: Session = Depends(get_session)):
    existing = session.exec(select(AdminUser).where(
        AdminUser.email == payload.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )
    hashed = hash_password(payload.password)
    db_user = AdminUser(
        name=payload.name,
        email=payload.email,
        password_hash=hashed,
        admin_role_id=1,
        is_active=True
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
