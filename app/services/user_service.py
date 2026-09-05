# =============================================
# services/user_service.py - Lógica de negocio
# =============================================

from fastapi import HTTPException
from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


def service_listar_usuarios(role=None, is_active=None):
    resultado = users_db
    if role:
        resultado = [u for u in resultado if u["role"] == role]
    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]
    return resultado


def service_obtener_usuario(user_id: int):
    usuario = next((u for u in users_db if u["id"] == user_id), None)
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return usuario


def service_crear_usuario(usuario: UserCreate):
    # Validar email duplicado
    if any(u["email"] == usuario.email for u in users_db):
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )
    nuevo_id = max(u["id"] for u in users_db) + 1
    nuevo = {
        "id":        nuevo_id,
        "name":      usuario.name,
        "email":     usuario.email,
        "role":      usuario.role,
        "is_active": usuario.is_active,
    }
    users_db.append(nuevo)
    return nuevo


def service_actualizar_usuario(user_id: int, usuario: UserUpdate):
    # Buscar usuario
    index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar email duplicado (ignorar el propio)
    if any(u["email"] == usuario.email and u["id"] != user_id for u in users_db):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    users_db[index] = {
        "id":        user_id,
        "name":      usuario.name,
        "email":     usuario.email,
        "role":      usuario.role,
        "is_active": usuario.is_active,
    }
    return users_db[index]


def service_patch_usuario(user_id: int, usuario: UserPatch):
    # Buscar usuario
    index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar que venga al menos un campo
    datos = usuario.model_dump(exclude_none=True)
    if not datos:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos un campo para actualizar"
        )

    # Validar email duplicado si viene email
    if "email" in datos:
        if any(u["email"] == datos["email"] and u["id"] != user_id for u in users_db):
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

    users_db[index].update(datos)
    return users_db[index]


def service_eliminar_usuario(user_id: int):
    index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    users_db.pop(index)
