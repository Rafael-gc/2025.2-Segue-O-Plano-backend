from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field


class PatientBase(SQLModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[date] = None


class Patient(PatientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    id: int
    created_at: datetime


class PatientUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[date] = None