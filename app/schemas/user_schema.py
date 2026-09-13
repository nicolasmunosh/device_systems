# =============================================
# schemas/user_schema.py - Schemas Pydantic v2
# =============================================

from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal, Optional
from datetime import datetime


# Modelo de entrada - crear usuario
class UserCreate(BaseModel):
    name:      str
    email:     EmailStr
    role:      Literal["admin", "support", "user"]
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres")
        return v.strip()


# Modelo de entrada - actualización completa PUT
class UserUpdate(BaseModel):
    name:      str
    email:     EmailStr
    role:      Literal["admin", "support", "user"]
    is_active: bool

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres")
        return v.strip()


# Modelo de entrada - actualización parcial PATCH
class UserPatch(BaseModel):
    name:      Optional[str]                              = None
    email:     Optional[EmailStr]                         = None
    role:      Optional[Literal["admin", "support", "user"]] = None
    is_active: Optional[bool]                             = None

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres")
        return v.strip() if v else v


# Modelo de salida - respuesta de la API
class UserResponse(BaseModel):
    id:         int
    name:       str
    email:      str
    role:       str
    is_active:  bool
    created_at: datetime

    model_config = {"from_attributes": True}
