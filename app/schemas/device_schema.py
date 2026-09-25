# =============================================
# schemas/device_schema.py - Schemas Device
# =============================================

from pydantic import BaseModel, field_validator
from typing import Literal, Optional
from datetime import datetime


class DeviceCreate(BaseModel):
    name:          str
    serial_number: str
    device_type:   Literal["laptop", "tablet", "proyector", "camara", "router", "monitor"]
    brand:         Optional[str] = None
    is_available:  bool = True

    @field_validator("name", "serial_number")
    @classmethod
    def no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip()


class DeviceUpdate(BaseModel):
    name:          str
    serial_number: str
    device_type:   Literal["laptop", "tablet", "proyector", "camara", "router", "monitor"]
    brand:         Optional[str] = None
    is_available:  bool


class DevicePatch(BaseModel):
    name:          Optional[str] = None
    serial_number: Optional[str] = None
    device_type:   Optional[Literal["laptop", "tablet", "proyector", "camara", "router", "monitor"]] = None
    brand:         Optional[str] = None
    is_available:  Optional[bool] = None


class DeviceResponse(BaseModel):
    id:            int
    name:          str
    serial_number: str
    device_type:   str
    brand:         Optional[str]
    is_available:  bool
    created_at:    datetime

    model_config = {"from_attributes": True}
