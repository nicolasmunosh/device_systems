# =============================================
# main.py - device_systems v3.0.0
# =============================================

from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes.user_routes import router
import app.models.user_model  # noqa: F401 — registra el modelo

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios con persistencia SQLAlchemy.",
    version="3.0.0",
    contact={
        "name":  "nicolasmunosh",
        "url":   "https://github.com/nicolasmunosh",
    },
)

app.include_router(router)


@app.get("/", tags=["Root"], summary="Inicio")
def inicio():
    return {
        "app":      "device_systems",
        "version":  "3.0.0",
        "database": "SQLite - device_systems.db",
        "docs":     "/docs",
        "redoc":    "/redoc"
    }
