from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CreateAdminUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class ReadAdminUser(BaseModel):
    model_config = ConfigDict(from_attribute=True)
    id: int
    name: str
    email: EmailStr
    admin_role_id: int
    is_active: bool


class UpdateAdminUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=1, max_length=50)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    email: EmailStr | None = None
    is_active: bool | None = None
    admin_role_id: int | None = None
