# =============================================
# user_routes.py - Rutas del recurso usuarios
# =============================================

from fastapi import APIRouter, HTTPException, Response
from typing import Optional
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

# Base de datos simulada en memoria
usuarios_db = [
    {"id": 1, "name": "Carlos Admin",   "email": "carlos@mail.com",  "role": "admin",   "is_active": True},
    {"id": 2, "name": "Maria Support",  "email": "maria@mail.com",   "role": "support", "is_active": True},
    {"id": 3, "name": "Juan User",      "email": "juan@mail.com",    "role": "user",    "is_active": False},
    {"id": 4, "name": "Ana User",       "email": "ana@mail.com",     "role": "user",    "is_active": True},
]


# ── GET /users ─────────────────────────────────────────────────────────────────
@router.get("/users", response_model=list[UserResponse])
def listar_usuarios(
    response: Response,
    role: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """
    Lista todos los usuarios.
    - Filtra por rol con ?role=admin
    - Filtra por estado con ?is_active=true
    """
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    resultado = usuarios_db

    if role:
        resultado = [u for u in resultado if u["role"] == role]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado


# ── GET /users/{user_id} ───────────────────────────────────────────────────────
@router.get("/users/{user_id}", response_model=UserResponse)
def obtener_usuario(user_id: int, response: Response):
    """Obtiene un usuario por su ID"""
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    usuario = next((u for u in usuarios_db if u["id"] == user_id), None)

    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado")

    return usuario


# ── POST /users ────────────────────────────────────────────────────────────────
@router.post("/users", response_model=UserResponse, status_code=201)
def crear_usuario(usuario: UserCreate, response: Response):
    """Registra un nuevo usuario validando los datos con Pydantic"""
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    # Verificar email duplicado
    email_existe = any(u["email"] == usuario.email for u in usuarios_db)
    if email_existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Crear nuevo usuario
    nuevo_id = max(u["id"] for u in usuarios_db) + 1
    nuevo_usuario = {
        "id":        nuevo_id,
        "name":      usuario.name,
        "email":     usuario.email,
        "role":      usuario.role,
        "is_active": usuario.is_active,
    }
    usuarios_db.append(nuevo_usuario)

    return nuevo_usuario
