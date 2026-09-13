# =============================================
# services/user_service.py - CRUD con SQLAlchemy
# =============================================

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


def service_listar_usuarios(db: Session, role: str = None, is_active: bool = None):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.order_by(User.name).all()


def service_obtener_usuario(db: Session, user_id: int):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return usuario


def service_obtener_por_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def service_crear_usuario(db: Session, usuario: UserCreate):
    # Verificar email duplicado
    if service_obtener_por_email(db, usuario.email):
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )
    nuevo = User(
        name      = usuario.name,
        email     = usuario.email,
        role      = usuario.role,
        is_active = usuario.is_active,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def service_actualizar_usuario(db: Session, user_id: int, usuario: UserUpdate):
    db_usuario = service_obtener_usuario(db, user_id)

    # Verificar email duplicado (ignorar el propio)
    existente = service_obtener_por_email(db, usuario.email)
    if existente and existente.id != user_id:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    db_usuario.name      = usuario.name
    db_usuario.email     = usuario.email
    db_usuario.role      = usuario.role
    db_usuario.is_active = usuario.is_active

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def service_patch_usuario(db: Session, user_id: int, usuario: UserPatch):
    db_usuario = service_obtener_usuario(db, user_id)

    datos = usuario.model_dump(exclude_none=True)
    if not datos:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos un campo para actualizar"
        )

    # Verificar email duplicado si viene email
    if "email" in datos:
        existente = service_obtener_por_email(db, datos["email"])
        if existente and existente.id != user_id:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

    for campo, valor in datos.items():
        setattr(db_usuario, campo, valor)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def service_eliminar_usuario(db: Session, user_id: int):
    db_usuario = service_obtener_usuario(db, user_id)
    db.delete(db_usuario)
    db.commit()
