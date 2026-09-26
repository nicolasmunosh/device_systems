# =============================================
# auth/auth_routes.py - Endpoints de autenticación
# =============================================

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.auth_schema import UserRegister, Token, AuthUserResponse
from app.auth.auth_service import service_registrar_usuario, service_autenticar_usuario
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_user
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=AuthUserResponse, status_code=201, summary="Registrar usuario")
@limiter.limit("3/minute")
def registrar(request: Request, datos: UserRegister, db: Session = Depends(get_db)):
    return service_registrar_usuario(db, datos)


@router.post("/login", response_model=Token, summary="Iniciar sesión")
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = service_autenticar_usuario(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=AuthUserResponse, summary="Usuario autenticado actual")
def me(usuario_actual=Depends(get_current_user)):
    return usuario_actual