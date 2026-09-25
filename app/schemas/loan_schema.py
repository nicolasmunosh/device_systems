# =============================================
# schemas/loan_schema.py - Schemas Loan
# =============================================

from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class LoanCreate(BaseModel):
    user_id:   int
    device_id: int


class LoanUpdate(BaseModel):
    status: Literal["active", "returned", "overdue"]


class LoanResponse(BaseModel):
    id:          int
    user_id:     int
    device_id:   int
    loan_date:   datetime
    return_date: Optional[datetime]
    status:      str

    model_config = {"from_attributes": True}


# Schema para mostrar info relacionada con joins
class UserBasic(BaseModel):
    id:    int
    name:  str
    email: str
    model_config = {"from_attributes": True}


class DeviceBasic(BaseModel):
    id:            int
    name:          str
    serial_number: str
    device_type:   str
    model_config = {"from_attributes": True}


class LoanDetailResponse(BaseModel):
    loan_id:     int
    status:      str
    loan_date:   datetime
    return_date: Optional[datetime]
    user:        UserBasic
    device:      DeviceBasic

    model_config = {"from_attributes": True}
