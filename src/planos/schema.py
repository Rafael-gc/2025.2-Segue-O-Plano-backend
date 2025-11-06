from datetime import date
from typing import Optional
from pydantic import BaseModel


class PlanoBase(BaseModel):
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    objetivo: Optional[str] = None


class PlanoCreate(PlanoBase):
    pass #paciente_id: int  # obrigatório para criar registro ligado a um paciente


class PlanoRead(PlanoBase):
    id: int
    paciente_id: int

    class Config:
        orm_mode = True


class PlanoUpdate(BaseModel):
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    objetivo: Optional[str] = None
