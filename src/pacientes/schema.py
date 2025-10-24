from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class PacienteBase(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = None
    gestante: Optional[bool] = None
    altura: Optional[float] = None


class PacienteCreate(PacienteBase):
    pass


class PacienteRead(PacienteBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = None
    gestante: Optional[bool] = None
    altura: Optional[float] = None
