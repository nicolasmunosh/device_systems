# =============================================
# main.py - device_systems v4.0.0
# =============================================

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.request_middleware import RequestLoggingMiddleware

from app.database.connection import engine, Base
from app.routes.user_routes   import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes   import router as loan_router
from app.auth.auth_routes     import router as auth_router


import app.models.user_model    # noqa
import app.models.device_model  # noqa
import app.models.loan_model    # noqa

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST segura para gestión de usuarios, dispositivos y préstamos.\n\n"
        "Incluye autenticación OAuth2 con JWT, control de acceso por roles, "
        "rate limiting y middleware de trazabilidad."
    ),
    version="4.0.0",
    contact={"name": "nicolasmunosh", "url": "https://github.com/nicolasmunosh"},
    openapi_tags=[
        {"name": "Auth", "description": "Registro, login y datos del usuario autenticado."},
        {"name": "Users", "description": "Gestión de usuarios (requiere autenticación)."},
        {"name": "Devices", "description": "Gestión de dispositivos (requiere rol admin o support)."},
        {"name": "Loans", "description": "Gestión de préstamos de dispositivos."},
        {"name": "Security", "description": "Notas sobre autenticación JWT, CORS y límites de peticiones."},
        {"name": "Root", "description": "Endpoint raíz de la API."},
    ],
)

from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# --- Configuración de CORS ---
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Middleware personalizado ---
app.add_middleware(RequestLoggingMiddleware)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"], summary="Inicio")
def inicio():
    return {
        "app":      "device_systems",
        "version":  "4.0.0",
        "recursos": ["/auth", "/users", "/devices", "/loans"],
        "docs":     "/docs",
        "redoc":    "/redoc"
    }