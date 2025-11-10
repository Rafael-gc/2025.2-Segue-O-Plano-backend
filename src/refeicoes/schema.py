from typing import Optional
from datetime import time
from pydantic import BaseModel


class RefeicaoBase(BaseModel):
    horario: Optional[time] = None
    descricao: Optional[str] = None

class RefeicaoCreate(RefeicaoBase):
    pass

class RefeicaoRead(RefeicaoBase):
    id: int
    plano_id: int

    class Config:
        orm_mode = True

class RefeicaoUpdate(BaseModel):
    horario: Optional[time] = None
    descricao: Optional[str] = None

    class Config:
        orm_mode = True