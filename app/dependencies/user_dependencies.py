# =============================================
# dependencies/user_dependencies.py - Depends()
# =============================================

from fastapi import HTTPException, Header
from app.data.users_db import users_db


def get_user_or_404(user_id: int):
    """Busca un usuario por ID, lanza 404 si no existe"""
    usuario = next((u for u in users_db if u["id"] == user_id), None)
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return usuario


def validar_email_duplicado(email: str, exclude_id: int = None):
    """Valida que el email no esté duplicado"""
    existe = any(
        u["email"] == email and u["id"] != exclude_id
        for u in users_db
    )
    if existe:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )


def get_api_config():
    """Retorna configuración general de la API"""
    return {
        "app":     "device_systems",
        "version": "2.0.0",
        "author":  "nicolasmunosh"
    }


def verificar_api_key(x_api_key: str = Header(default=None)):
    """Simula autenticación básica mediante cabecera X-Api-Key"""
    if x_api_key != "device-secret-key":
        raise HTTPException(
            status_code=401,
            detail="API Key inválida o no proporcionada"
        )
    return x_api_key
