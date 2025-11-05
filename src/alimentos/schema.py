from pydantic import BaseModel
from typing import Optional

class AlimentoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    kcal: Optional[float] = None
    proteinas: Optional[float] = None
    carboidratos: Optional[float] = None
    lipideos: Optional[float] = None

class AlimentoCreate(AlimentoBase):
    pass

class AlimentoRead(AlimentoBase):
    id: int

    class Config:
        orm_mode = True

class AlimentoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    kcal: Optional[float] = None
    proteinas: Optional[float] = None
    carboidratos: Optional[float] = None
    lipideos: Optional[float] = None

    class Config:
        orm_mode = True

# Schemas para associação refeicao_alimento (mantidos)
class RefeicaoAlimentoCreate(BaseModel):
    alimento_id: int
    quantidade: Optional[float] = None
    medida: Optional[str] = None

class RefeicaoAlimentoRead(BaseModel):
    alimento: AlimentoRead
    quantidade: Optional[float] = None
    medida: Optional[str] = None

    class Config:
        orm_mode = True