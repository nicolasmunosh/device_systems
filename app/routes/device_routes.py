# =============================================
# routes/device_routes.py - CRUD Dispositivos
# =============================================

from fastapi import APIRouter, Response, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.services.device_service import (
    service_listar_dispositivos,
    service_obtener_dispositivo,
    service_crear_dispositivo,
    service_actualizar_dispositivo,
    service_patch_dispositivo,
    service_eliminar_dispositivo,
)
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/devices", tags=["Devices"])


def add_headers(response: Response):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "4.0.0"


@router.get("", response_model=list[DeviceResponse], summary="Listar dispositivos")
def listar_dispositivos(
    response: Response,
    db: Session = Depends(get_db),
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None
):
    add_headers(response)
    return service_listar_dispositivos(db, device_type, is_available, brand, search)


@router.get("/{device_id}", response_model=DeviceResponse, summary="Obtener dispositivo por ID")
def obtener_dispositivo(device_id: int, response: Response, db: Session = Depends(get_db)):
    add_headers(response)
    return service_obtener_dispositivo(db, device_id)


@router.post("", response_model=DeviceResponse, status_code=201, summary="Crear dispositivo")
def crear_dispositivo(dispositivo: DeviceCreate, response: Response, db: Session = Depends(get_db)):
    add_headers(response)
    return service_crear_dispositivo(db, dispositivo)


@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo completo")
def actualizar_dispositivo(device_id: int, dispositivo: DeviceUpdate, response: Response, db: Session = Depends(get_db)):
    add_headers(response)
    return service_actualizar_dispositivo(db, device_id, dispositivo)


@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo parcial")
def patch_dispositivo(device_id: int, dispositivo: DevicePatch, response: Response, db: Session = Depends(get_db)):
    add_headers(response)
    return service_patch_dispositivo(db, device_id, dispositivo)


@router.delete("/{device_id}", status_code=204, summary="Eliminar dispositivo")
def eliminar_dispositivo(device_id: int, db: Session = Depends(get_db)):
    service_eliminar_dispositivo(db, device_id)
