# =============================================
# routes/loan_routes.py - Gestión de préstamos
# =============================================

from fastapi import APIRouter, Response, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import (
    service_listar_prestamos,
    service_obtener_prestamo,
    service_crear_prestamo,
    service_devolver_prestamo,
    service_prestamos_usuario,
    service_prestamos_dispositivo,
    _loan_to_detail,
)
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get("", response_model=list[LoanDetailResponse], summary="Listar préstamos con filtros")
def listar_prestamos(
    response: Response,
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None
):
    loans = service_listar_prestamos(db, status, user_email, device_type)
    return [_loan_to_detail(l) for l in loans]


@router.get("/details", response_model=list[LoanDetailResponse], summary="Listar préstamos con detalle")
def listar_prestamos_detalle(response: Response, db: Session = Depends(get_db)):
    loans = service_listar_prestamos(db)
    return [_loan_to_detail(l) for l in loans]


@router.get("/{loan_id}", response_model=LoanDetailResponse, summary="Obtener préstamo por ID")
def obtener_prestamo(loan_id: int, response: Response, db: Session = Depends(get_db)):
    loan = service_obtener_prestamo(db, loan_id)
    return _loan_to_detail(loan)


@router.post("", response_model=LoanDetailResponse, status_code=201, summary="Crear préstamo")
def crear_prestamo(prestamo: LoanCreate, response: Response, db: Session = Depends(get_db)):
    loan = service_crear_prestamo(db, prestamo)
    return _loan_to_detail(loan)


@router.patch("/{loan_id}/return", response_model=LoanDetailResponse, summary="Devolver dispositivo")
def devolver_prestamo(loan_id: int, response: Response, db: Session = Depends(get_db)):
    loan = service_devolver_prestamo(db, loan_id)
    return _loan_to_detail(loan)
