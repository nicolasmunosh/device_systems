# =============================================
# auth/auth_service.py - Lógica de autenticación
# =============================================

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.auth_schema import UserRegister, UserLogin
from app.auth.security import get_password_hash, verify_password, create_access_token


def service_registrar_usuario(db: Session, datos: UserRegister) -> User:
    """Registra un nuevo usuario con contraseña hasheada."""
    existente = db.query(User).filter(User.email == datos.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )

    nuevo_usuario = User(
        name=datos.name,
        email=datos.email,
        hashed_password=get_password_hash(datos.password),
        role=datos.role,
        is_active=True,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def service_autenticar_usuario(db: Session, datos: UserLogin) -> str:
    """Valida credenciales y retorna un token JWT si son correctas."""
    usuario = db.query(User).filter(User.email == datos.email).first()

    if not usuario or not verify_password(datos.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )

    token = create_access_token(data={"sub": usuario.email, "role": usuario.role})
    return token