# =============================================
# user_schema.py - Modelos de usuario con Pydantic v2
# =============================================

from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal, Optional


# Modelo de entrada - para crear un usuario
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


# Modelo de salida - lo que devuelve la API
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}
