from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from pacientes.schema import PacienteCreate, PacienteRead, PacienteUpdate
from . import repository

router = APIRouter(prefix="/pacientes", tags=["pacientes"])


@router.get("/", response_model=List[PacienteRead])
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return repository.list_pacientes(db, skip=skip, limit=limit)


@router.post("/", response_model=PacienteRead, status_code=status.HTTP_201_CREATED)
def criar_paciente(payload: PacienteCreate, db: Session = Depends(get_session)):
    return repository.create_paciente(db, payload)


@router.get("/{paciente_id}", response_model=PacienteRead)
def obter_paciente(paciente_id: int, db: Session = Depends(get_session)):
    p = repository.get_paciente(db, paciente_id)
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return p


@router.put("/{paciente_id}", response_model=PacienteRead)
def atualizar_paciente(paciente_id: int, payload: PacienteUpdate, db: Session = Depends(get_session)):
    p = repository.update_paciente(db, paciente_id, payload)
    if not p:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return p


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_paciente(paciente_id: int, db: Session = Depends(get_session)):
    ok = repository.delete_paciente(db, paciente_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return None
