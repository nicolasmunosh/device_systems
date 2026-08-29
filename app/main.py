# =============================================
# main.py - Punto de entrada de device_systems
# =============================================

from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="device_systems",
    description="API REST para gestión de usuarios del sistema device_systems",
    version="1.0",
)

# Registrar las rutas de usuarios
app.include_router(router)


@app.get("/")
def inicio():
    return {
        "app":     "device_systems",
        "version": "1.0",
        "docs":    "/docs"
    }
