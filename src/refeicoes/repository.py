from typing import List, Optional
from sqlalchemy.orm import Session
from models.models import Refeicao, Plano
from refeicoes.schema import RefeicaoCreate, RefeicaoUpdate

def _check_plano_belongs_to_paciente(db: Session, paciente_id: int, plano_id: int) -> None:
    plano = db.get(Plano, plano_id)
    if not plano or getattr(plano, "paciente_id", None) != paciente_id:
        raise ValueError("plano_nao_encontrado")


def list_refeicoes(db: Session, paciente_id: int, plano_id: int, skip: int = 0, limit: int = 100) -> List[Refeicao]:
    _check_plano_belongs_to_paciente(db, paciente_id, plano_id)
    return db.query(Refeicao).filter(Refeicao.plano_id == plano_id).offset(skip).limit(limit).all()


def get_refeicao(db: Session, paciente_id: int, plano_id: int, refeicao_id: int) -> Optional[Refeicao]:
    _check_plano_belongs_to_paciente(db, paciente_id, plano_id)
    r = db.get(Refeicao, refeicao_id)
    if not r or r.plano_id != plano_id:
        return None
    return r


def create_refeicao(db: Session, paciente_id: int, plano_id: int, payload: RefeicaoCreate) -> Refeicao:
    _check_plano_belongs_to_paciente(db, paciente_id, plano_id)
    r = Refeicao(plano_id=plano_id, **payload.dict())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def update_refeicao(db: Session, paciente_id: int, plano_id: int, refeicao_id: int, payload: RefeicaoUpdate) -> Optional[Refeicao]:
    _check_plano_belongs_to_paciente(db, paciente_id, plano_id)
    r = db.get(Refeicao, refeicao_id)
    if not r or r.plano_id != plano_id:
        return None
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(r, key, value)
    db.commit()
    db.refresh(r)
    return r


def delete_refeicao(db: Session, paciente_id: int, plano_id: int, refeicao_id: int) -> bool:
    _check_plano_belongs_to_paciente(db, paciente_id, plano_id)
    r = db.get(Refeicao, refeicao_id)
    if not r or r.plano_id != plano_id:
        return False
    db.delete(r)
    db.commit()
    return True