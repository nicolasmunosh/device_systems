# =============================================
# routes/user_routes.py - CRUD usuarios + loans
# =============================================

from fastapi import APIRouter, Response, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services.user_service import (
    service_listar_usuarios,
    service_obtener_usuario,
    service_crear_usuario,
    service_actualizar_usuario,
    service_patch_usuario,
    service_eliminar_usuario,
)
from app.services.loan_service import service_prestamos_usuario, _loan_to_detail
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/users", tags=["Users"])


def add_headers(response: Response):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "4.0.0"


@router.get("", response_model=list[UserResponse], summary="Listar usuarios")
def listar_usuarios(response: Response, db: Session = Depends(get_db), role: Optional[str] = None, is_active: Optional[bool] = None):
    add_headers(response)
    return service_listar_usuarios(db, role, is_active)


@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID")
def obtener_usuario(user_id: int, response: Response, db: Session = Depends(get_db)):
    add_headers(response)
    return service_obtener_usuario(db, user_id)


@router.get("/{user_id}/loans", response_model=list[LoanDetailResponse], summary="Préstamos de un usuario")
def prestamos_usuario(user_id: int, response: Response, db: Session = Depends(get_db)):
    add_headers(response)
    loans = service_prestamos_usuario(db, user_id)
    return [_loan_to_detail(l) for l in loans]


@router.post("", response_model=UserResponse, status_code=201, summary="Crear usuario")
def crear_usuario(usuario: UserCreate, response: Response, db: Session = Depends(get_db)):
    add_headers(response)
    return service_crear_usuario(db, usuario)


@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar usuario completo")
def actualizar_usuario(user_id: int, usuario: UserUpdate, response: Response, db: Session = Depends(get_db)):
    add_headers(response)
    return service_actualizar_usuario(db, user_id, usuario)


@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar usuario parcial")
def patch_usuario(user_id: int, usuario: UserPatch, response: Response, db: Session = Depends(get_db)):
    add_headers(response)
    return service_patch_usuario(db, user_id, usuario)


@router.delete("/{user_id}", status_code=204, summary="Eliminar usuario")
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    service_eliminar_usuario(db, user_id)
