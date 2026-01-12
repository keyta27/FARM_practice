from fastapi import APIRouter, HTTPException, Depends, status, Query, Path
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


@router.get("/", response_model=list[ReadAdminUser])
def get_admin_users(
        session: Session = Depends(get_session),
        offset: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100)):
    all_admin_user = session.exec(
        select(AdminUser).order_by(AdminUser.id).offset(offset).limit(limit)).all()

    return all_admin_user


@router.get("/{admin_user_id}", response_model=ReadAdminUser)
def get_admin_user_by_id(admin_user_id: int = Path(..., ge=1), session: Session = Depends(get_session)):

    get_user = session.exec(select(AdminUser).where(
        AdminUser.id == admin_user_id)).first()

    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin user ot found")

    return get_user


@router.patch("/{admin_user_id}", response_model=ReadAdminUser)
def update_admin_user(payload: UpdateAdminUser, admin_user_id: int = Path(..., ge=1), session: Session = Depends(get_session)):
    db_admin_user = session.exec(select(AdminUser).where(
        AdminUser.id == admin_user_id)).first()

    if not db_admin_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found"
        )
    update_data = payload.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"] is not None:
        db_admin_user.password_hash = hash_password(
            update_data.pop("password"))

    db_admin_user.sqlmodel_update(update_data)

    session.add(db_admin_user)
    session.commit()
    session.refresh(db_admin_user)
    return db_admin_user


@router.delete("/{admin_user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin_user(admin_user_id: int = Path(..., ge=1), session: Session = Depends(get_session)):
    db_user = session.exec(select(AdminUser).where(
        AdminUser.id == admin_user_id)).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found")

    if not db_user.is_active:
        return

    db_user.is_active = False

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
