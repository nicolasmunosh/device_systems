# =============================================
# main.py - device_systems v4.0.0
# =============================================

from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes.user_routes   import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes   import router as loan_router

import app.models.user_model    # noqa
import app.models.device_model  # noqa
import app.models.loan_model    # noqa

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios, dispositivos y préstamos con SQLAlchemy y Alembic.",
    version="4.0.0",
    contact={"name": "nicolasmunosh", "url": "https://github.com/nicolasmunosh"},
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"], summary="Inicio")
def inicio():
    return {
        "app":      "device_systems",
        "version":  "4.0.0",
        "recursos": ["/users", "/devices", "/loans"],
        "docs":     "/docs",
        "redoc":    "/redoc"
    }
