from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
from models.models import Alimento, Refeicao, refeicao_alimento_table

from alimentos.schema import AlimentoCreate, AlimentoUpdate, RefeicaoAlimentoCreate

def list_alimentos(db: Session, skip: int = 0, limit: int = 100) -> List[Alimento]:
    return db.query(Alimento).offset(skip).limit(limit).all()

def get_alimento(db: Session, alimento_id: int) -> Optional[Alimento]:
    return db.get(Alimento, alimento_id)

def create_alimento(db: Session, payload: AlimentoCreate) -> Alimento:
    a = Alimento(**payload.dict())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

def update_alimento(db: Session, alimento_id: int, payload: AlimentoUpdate) -> Optional[Alimento]:
    a = db.get(Alimento, alimento_id)
    if not a:
        return None
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(a, key, value)
    db.commit()
    db.refresh(a)
    return a

def delete_alimento(db: Session, alimento_id: int) -> bool:
    a = db.get(Alimento, alimento_id)
    if not a:
        return False
    db.delete(a)
    db.commit()
    return True

# ----------------- funções para a tabela associativa -----------------
def add_alimento_to_refeicao(db: Session, refeicao_id: int, payload: RefeicaoAlimentoCreate) -> Dict[str, Any]:
    # garante que refeicao e alimento existam
    r = db.get(Refeicao, refeicao_id)
    if not r:
        raise ValueError("refeicao_nao_encontrada")
    a = db.get(Alimento, payload.alimento_id)
    if not a:
        raise ValueError("alimento_nao_encontrado")

    stmt = insert(refeicao_alimento_table).values(
        refeicao_id=refeicao_id,
        alimento_id=payload.alimento_id,
        quantidade=payload.quantidade,
        medida=payload.medida
    )
    db.execute(stmt)
    db.commit()
    return {"refeicao_id": refeicao_id, "alimento_id": payload.alimento_id, "quantidade": payload.quantidade, "medida": payload.medida}

def list_alimentos_da_refeicao(db: Session, refeicao_id: int) -> List[Dict[str, Any]]:
    stmt = (
        select(
            Alimento,
            refeicao_alimento_table.c.quantidade,
            refeicao_alimento_table.c.medida
        )
        .join(refeicao_alimento_table, Alimento.id == refeicao_alimento_table.c.alimento_id)
        .where(refeicao_alimento_table.c.refeicao_id == refeicao_id)
    )
    res = db.execute(stmt).all()
    result = []
    for alimento_row, quantidade, medida in res:
        # alimento_row é instância de Alimento via ORM -> pode usar atributos
        result.append({
            "alimento": alimento_row,
            "quantidade": quantidade,
            "medida": medida
        })
    return result

def update_alimento_refeicao(db: Session, refeicao_id: int, alimento_id: int, quantidade: Optional[float], medida: Optional[str]) -> bool:
    stmt = update(refeicao_alimento_table).where(
        (refeicao_alimento_table.c.refeicao_id == refeicao_id) &
        (refeicao_alimento_table.c.alimento_id == alimento_id)
    ).values(quantidade=quantidade, medida=medida)
    res = db.execute(stmt)
    db.commit()
    return res.rowcount > 0

def remove_alimento_from_refeicao(db: Session, refeicao_id: int, alimento_id: int) -> bool:
    stmt = delete(refeicao_alimento_table).where(
        (refeicao_alimento_table.c.refeicao_id == refeicao_id) &
        (refeicao_alimento_table.c.alimento_id == alimento_id)
    )
    res = db.execute(stmt)
    db.commit()
    return res.rowcount > 0