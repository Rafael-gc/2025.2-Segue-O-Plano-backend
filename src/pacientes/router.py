from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session

from database import get_session
from models.models import PatientCreate, PatientRead, PatientUpdate
from . import repository

router = APIRouter(prefix="/pacientes", tags=["pacientes"])


@router.get("/", response_model=List[PatientRead])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return repository.list_patients(db, skip=skip, limit=limit)


@router.post("/", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_session)):
    return repository.create_patient(db, payload)


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_session)):
    p = repository.get_patient(db, patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p


@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_session)):
    p = repository.update_patient(db, patient_id, payload)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_session)):
    ok = repository.delete_patient(db, patient_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Patient not found")
    return None
