# =============================================
# routes/user_routes.py - CRUD completo
# =============================================

from fastapi import APIRouter, Response, Depends
from typing import Optional

from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.services.user_service import (
    service_listar_usuarios,
    service_obtener_usuario,
    service_crear_usuario,
    service_actualizar_usuario,
    service_patch_usuario,
    service_eliminar_usuario,
)
from app.dependencies.user_dependencies import get_user_or_404

router = APIRouter(prefix="/users", tags=["Users"])


def add_headers(response: Response):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "2.0.0"


# ── GET /users ─────────────────────────────────────────────────────────────────
@router.get(
    "",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Permite filtrar por rol y estado activo.",
    response_description="Lista de usuarios registrados"
)
def listar_usuarios(
    response: Response,
    role: Optional[str] = None,
    is_active: Optional[bool] = None
):
    add_headers(response)
    return service_listar_usuarios(role, is_active)


# ── GET /users/{user_id} ───────────────────────────────────────────────────────
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico usando su ID como Path Parameter.",
    response_description="Usuario encontrado"
)
def obtener_usuario(response: Response, usuario=Depends(get_user_or_404)):
    add_headers(response)
    return usuario


# ── POST /users ────────────────────────────────────────────────────────────────
@router.post(
    "",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Registra un nuevo usuario. Valida datos con Pydantic y evita correos duplicados.",
    response_description="Usuario creado exitosamente"
)
def crear_usuario(usuario: UserCreate, response: Response):
    add_headers(response)
    return service_crear_usuario(usuario)


# ── PUT /users/{user_id} ───────────────────────────────────────────────────────
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza completamente la información de un usuario existente.",
    response_description="Usuario actualizado"
)
def actualizar_usuario(
    user_id: int,
    usuario: UserUpdate,
    response: Response
):
    add_headers(response)
    return service_actualizar_usuario(user_id, usuario)


# ── PATCH /users/{user_id} ─────────────────────────────────────────────────────
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente",
    description="Modifica solo los campos enviados. Si no se envía ningún campo retorna 400.",
    response_description="Usuario actualizado parcialmente"
)
def patch_usuario(
    user_id: int,
    usuario: UserPatch,
    response: Response
):
    add_headers(response)
    return service_patch_usuario(user_id, usuario)


# ── DELETE /users/{user_id} ────────────────────────────────────────────────────
@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario por su ID. Retorna 204 si fue eliminado, 404 si no existe.",
    response_description="Usuario eliminado"
)
def eliminar_usuario(user_id: int):
    service_eliminar_usuario(user_id)
