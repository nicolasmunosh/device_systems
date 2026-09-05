# =============================================
# schemas/user_schema.py - Modelos Pydantic v2
# =============================================

from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal, Optional


# Modelo de entrada - crear usuario (todos los campos requeridos)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres")
        return v.strip()


# Modelo de entrada - actualización completa PUT (todos los campos requeridos)
class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres")
        return v.strip()


# Modelo de entrada - actualización parcial PATCH (todos los campos opcionales)
class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal["admin", "support", "user"]] = None
    is_active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres")
        return v.strip() if v else v


# Modelo de salida - lo que devuelve la API
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}
