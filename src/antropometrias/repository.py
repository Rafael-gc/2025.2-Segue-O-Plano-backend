from typing import List, Optional
from sqlalchemy.orm import Session
from antropometrias.schema import AntropometriaCreate, AntropometriaUpdate
from models.models import Antropometria


def list_antropometrias(db: Session, paciente_id: int) -> List[Antropometria]:
    return db.query(Antropometria).filter(Antropometria.paciente_id == paciente_id).all()


def get_antropometria(db: Session, paciente_id: int, antropometria_id: int) -> Optional[Antropometria]:
    return (
        db.query(Antropometria)
        .filter(
            Antropometria.id == antropometria_id,
            Antropometria.paciente_id == paciente_id
        )
        .first()
    )


def create_antropometria(db: Session, paciente_id: int, payload: AntropometriaCreate) -> Antropometria:
    antropometria = Antropometria(**payload.dict(), paciente_id=paciente_id)
    db.add(antropometria)
    db.commit()
    db.refresh(antropometria)
    return antropometria


def update_antropometria(db: Session, paciente_id: int, antropometria_id: int, payload: AntropometriaUpdate) -> Optional[Antropometria]:
    antropometria = get_antropometria(db, paciente_id, antropometria_id)
    if not antropometria:
        return None

    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(antropometria, key, value)

    db.commit()
    db.refresh(antropometria)
    return antropometria


def delete_antropometria(db: Session, paciente_id: int, antropometria_id: int) -> bool:
    antropometria = get_antropometria(db, paciente_id, antropometria_id)
    if not antropometria:
        return False

    db.delete(antropometria)
    db.commit()
    return True
