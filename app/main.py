# =============================================
# main.py - device_systems v2.0.0
# =============================================

from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems. "
                "Incluye CRUD completo, manejo de errores, Dependency Injection y documentación OpenAPI.",
    version="2.0.0",
    contact={
        "name": "nicolasmunosh",
        "url":  "https://github.com/nicolasmunosh",
    },
    license_info={
        "name": "MIT",
    },
)

app.include_router(router)


@app.get("/", tags=["Root"], summary="Inicio", description="Información general de la API")
def inicio():
    return {
        "app":     "device_systems",
        "version": "2.0.0",
        "docs":    "/docs",
        "redoc":   "/redoc"
    }
