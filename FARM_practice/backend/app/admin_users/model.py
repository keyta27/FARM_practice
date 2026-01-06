from sqlmodel import SQLModel, Field


class AdminUser(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, index=True)
    email: str = Field(max_length=255, index=True, unique=True)
    password_hash: str = Field(max_length=255)
    # admin_role_id: int = Field(foreign_key="admin_roles.id")
    admin_role_id: int = Field(default=1)
    is_active: bool = Field(default=True)
