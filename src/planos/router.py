from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from database import get_session
from planos.schema import PlanoCreate, PlanoRead, PlanoUpdate
from . import repository

router = APIRouter(prefix="/pacientes/{paciente_id}/planos", tags=["planos"])


@router.get("/", response_model=List[PlanoRead])
def listar_planos(paciente_id: int, db: Session = Depends(get_session)):
    return repository.list_planos(db, paciente_id)


@router.post("/", response_model=PlanoRead, status_code=status.HTTP_201_CREATED)
def criar_plano(paciente_id: int, payload: PlanoCreate, db: Session = Depends(get_session)):
    return repository.create_plano(db, paciente_id, payload)


@router.get("/{plano_id}", response_model=PlanoRead)
def obter_plano(paciente_id: int, plano_id: int, db: Session = Depends(get_session)):
    plano = repository.get_plano(db, paciente_id, plano_id)
    if not plano:
        raise HTTPException(status_code=404, detail="Registro de plano não encontrado")
    return plano


@router.put("/{plano_id}", response_model=PlanoRead)
def atualizar_plano(paciente_id: int, plano_id: int, payload: PlanoUpdate, db: Session = Depends(get_session)):
    plano = repository.update_plano(db, paciente_id, plano_id, payload)
    if not plano:
        raise HTTPException(status_code=404, detail="Registro de plano não encontrado")
    return plano


@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_plano(paciente_id: int, plano_id: int, db: Session = Depends(get_session)):
    ok = repository.delete_plano(db, paciente_id, plano_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Registro de plano não encontrado")
    return None
