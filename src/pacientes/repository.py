from typing import List, Optional
from sqlmodel import select, Session
from models.models import Patient, PatientCreate, PatientUpdate


def list_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
    stmt = select(Patient).offset(skip).limit(limit)
    return db.exec(stmt).all()


def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
    return db.get(Patient, patient_id)


def create_patient(db: Session, payload: PatientCreate) -> Patient:
    p = Patient.from_orm(payload)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def update_patient(db: Session, patient_id: int, payload: PatientUpdate) -> Optional[Patient]:
    p = db.get(Patient, patient_id)
    if not p:
        return None
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(p, key, value)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def delete_patient(db: Session, patient_id: int) -> bool:
    p = db.get(Patient, patient_id)
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True