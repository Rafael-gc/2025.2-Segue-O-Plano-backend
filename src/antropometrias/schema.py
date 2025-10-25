from datetime import date
from typing import Optional
from pydantic import BaseModel


class AntropometriaBase(BaseModel):
    data: Optional[date] = None
    peso_atual: Optional[float] = None
    peso_habitual: Optional[float] = None
    dobra_triceps: Optional[float] = None
    dobra_biceps: Optional[float] = None
    dobra_subescapular: Optional[float] = None
    dobra_suprailiaca: Optional[float] = None
    circunferencia_braco: Optional[float] = None
    circunferencia_cintura: Optional[float] = None
    circunferencia_abdomen: Optional[float] = None
    circunferencia_quadril: Optional[float] = None
    circunferencia_panturrilha: Optional[float] = None
    observacoes: Optional[str] = None


class AntropometriaCreate(AntropometriaBase):
    pass #paciente_id: int  # obrigatório para criar registro ligado a um paciente


class AntropometriaRead(AntropometriaBase):
    id: int
    paciente_id: int

    class Config:
        orm_mode = True


class AntropometriaUpdate(BaseModel):
    data: Optional[date] = None
    peso_atual: Optional[float] = None
    peso_habitual: Optional[float] = None
    dobra_triceps: Optional[float] = None
    dobra_biceps: Optional[float] = None
    dobra_subescapular: Optional[float] = None
    dobra_suprailiaca: Optional[float] = None
    circunferencia_braco: Optional[float] = None
    circunferencia_cintura: Optional[float] = None
    circunferencia_abdomen: Optional[float] = None
    circunferencia_quadril: Optional[float] = None
    circunferencia_panturrilha: Optional[float] = None
    observacoes: Optional[str] = None
