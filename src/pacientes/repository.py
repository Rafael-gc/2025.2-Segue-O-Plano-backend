from typing import List, Optional
from sqlalchemy.orm import Session
from pacientes.schema import PacienteCreate, PacienteRead, PacienteUpdate
from models.models import Paciente


def list_pacientes(db: Session, skip: int = 0, limit: int = 100) -> List[Paciente]:
    return db.query(Paciente).offset(skip).limit(limit).all()


def get_paciente(db: Session, paciente_id: int) -> Optional[Paciente]:
    return db.get(Paciente, paciente_id)


def create_paciente(db: Session, payload: PacienteCreate) -> Paciente:
    p = Paciente(**payload.dict())  # cria o objeto diretamente
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def update_paciente(db: Session, paciente_id: int, payload: PacienteUpdate) -> Optional[Paciente]:
    p = db.get(Paciente, paciente_id)
    if not p:
        return None
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return p


def delete_paciente(db: Session, paciente_id: int) -> bool:
    p = db.get(Paciente, paciente_id)
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True
