# =============================================
# services/loan_service.py - Gestión préstamos
# =============================================

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException
from datetime import datetime
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse


def service_listar_prestamos(
    db: Session,
    status: str = None,
    user_email: str = None,
    device_type: str = None
):
    query = db.query(Loan).options(
        joinedload(Loan.user),
        joinedload(Loan.device)
    )
    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.join(User).filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.join(Device).filter(Device.device_type == device_type)
    return query.all()


def service_obtener_prestamo(db: Session, loan_id: int):
    loan = db.query(Loan).options(
        joinedload(Loan.user),
        joinedload(Loan.device)
    ).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail=f"Préstamo con ID {loan_id} no encontrado")
    return loan


def service_crear_prestamo(db: Session, prestamo: LoanCreate):
    # Validar usuario
    usuario = db.query(User).filter(User.id == prestamo.user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validar dispositivo
    dispositivo = db.query(Device).filter(Device.id == prestamo.device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    # Validar disponibilidad
    if not dispositivo.is_available:
        raise HTTPException(status_code=409, detail="El dispositivo no está disponible")

    # Crear préstamo
    nuevo = Loan(
        user_id=prestamo.user_id,
        device_id=prestamo.device_id,
        status="active"
    )
    dispositivo.is_available = False
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return service_obtener_prestamo(db, nuevo.id)


def service_devolver_prestamo(db: Session, loan_id: int):
    loan = db.query(Loan).options(
        joinedload(Loan.user),
        joinedload(Loan.device)
    ).filter(Loan.id == loan_id).first()

    if not loan:
        raise HTTPException(status_code=404, detail=f"Préstamo con ID {loan_id} no encontrado")

    if loan.status == "returned":
        raise HTTPException(status_code=409, detail="El préstamo ya fue devuelto")

    # Marcar como devuelto
    loan.status      = "returned"
    loan.return_date = datetime.utcnow()

    # Actualizar disponibilidad del dispositivo
    dispositivo = db.query(Device).filter(Device.id == loan.device_id).first()
    if dispositivo:
        dispositivo.is_available = True

    db.commit()
    db.refresh(loan)

    return service_obtener_prestamo(db, loan_id)


def service_prestamos_usuario(db: Session, user_id: int):
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Loan).options(
        joinedload(Loan.user),
        joinedload(Loan.device)
    ).filter(Loan.user_id == user_id).all()


def service_prestamos_dispositivo(db: Session, device_id: int):
    dispositivo = db.query(Device).filter(Device.id == device_id).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db.query(Loan).options(
        joinedload(Loan.user),
        joinedload(Loan.device)
    ).filter(Loan.device_id == device_id).all()


def _loan_to_detail(loan: Loan) -> dict:
    return {
        "loan_id":     loan.id,
        "status":      loan.status,
        "loan_date":   loan.loan_date,
        "return_date": loan.return_date,
        "user":        loan.user,
        "device":      loan.device,
    }
