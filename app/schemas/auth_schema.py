# =============================================
# schemas/auth_schema.py - Schemas de autenticación
# =============================================

import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Literal


# --- Registro de usuario ---
class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico único")
    password: str = Field(..., min_length=8, description="Contraseña segura")
    role: Literal["admin", "support", "user"] = Field(default="user")

    @field_validator("password")
    @classmethod
    def validar_password_segura(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contraseña no puede contener espacios en blanco")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe tener al menos una letra mayúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe tener al menos una letra minúscula")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe tener al menos un número")
        return v

    @field_validator("name")
    @classmethod
    def name_min_length(cls, v: str) -> str:
        if len(v.strip()) < 3:
            raise ValueError("El nombre debe tener mínimo 3 caracteres")
        return v.strip()


# --- Login de usuario ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- Respuesta con el token JWT ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Datos codificados dentro del token ---
class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None


# --- Respuesta del usuario autenticado (sin password) ---
class AuthUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str
    is_active: bool