from typing import List, Optional
from sqlalchemy.orm import Session
from planos.schema import PlanoCreate, PlanoRead, PlanoUpdate
from models.models import Plano


def list_planos(db: Session, paciente_id: int) -> List[Plano]:
    return db.query(Plano).filter(Plano.paciente_id == paciente_id).all()


def get_plano(db: Session, paciente_id: int, plano_id: int) -> Optional[Plano]:
    return (
        db.query(Plano)
        .filter(
            Plano.id == plano_id,
            Plano.paciente_id == paciente_id
        )
        .first()
    )


def create_plano(db: Session, paciente_id: int, payload: PlanoCreate) -> Plano:
    plano = Plano(**payload.dict(), paciente_id=paciente_id)
    db.add(plano)
    db.commit()
    db.refresh(plano)
    return plano


def update_plano(db: Session, paciente_id: int, plano_id: int, payload: PlanoUpdate) -> Optional[Plano]:
    plano = get_plano(db, paciente_id, plano_id)
    if not plano:
        return None

    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(plano, key, value)

    db.commit()
    db.refresh(plano)
    return plano


def delete_plano(db: Session, paciente_id: int, plano_id: int) -> bool:
    plano = get_plano(db, paciente_id, plano_id)
    if not plano:
        return False

    db.delete(plano)
    db.commit()
    return True
