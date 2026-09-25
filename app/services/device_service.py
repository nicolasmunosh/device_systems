# =============================================
# services/device_service.py - CRUD Devices
# =============================================

from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch


def service_listar_dispositivos(
    db: Session,
    device_type: str = None,
    is_available: bool = None,
    brand: str = None,
    search: str = None
):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
            )
        )
    return query.order_by(Device.name).all()


def service_obtener_dispositivo(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con ID {device_id} no encontrado")
    return device


def service_crear_dispositivo(db: Session, dispositivo: DeviceCreate):
    if db.query(Device).filter(Device.serial_number == dispositivo.serial_number).first():
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    nuevo = Device(**dispositivo.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def service_actualizar_dispositivo(db: Session, device_id: int, dispositivo: DeviceUpdate):
    db_device = service_obtener_dispositivo(db, device_id)
    existente = db.query(Device).filter(Device.serial_number == dispositivo.serial_number).first()
    if existente and existente.id != device_id:
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    for campo, valor in dispositivo.model_dump().items():
        setattr(db_device, campo, valor)
    db.commit()
    db.refresh(db_device)
    return db_device


def service_patch_dispositivo(db: Session, device_id: int, dispositivo: DevicePatch):
    db_device = service_obtener_dispositivo(db, device_id)
    datos = dispositivo.model_dump(exclude_none=True)
    if not datos:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un campo")
    if "serial_number" in datos:
        existente = db.query(Device).filter(Device.serial_number == datos["serial_number"]).first()
        if existente and existente.id != device_id:
            raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    for campo, valor in datos.items():
        setattr(db_device, campo, valor)
    db.commit()
    db.refresh(db_device)
    return db_device


def service_eliminar_dispositivo(db: Session, device_id: int):
    db_device = service_obtener_dispositivo(db, device_id)
    db.delete(db_device)
    db.commit()
