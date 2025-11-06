from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from antropometrias.schema import AntropometriaCreate, AntropometriaRead, AntropometriaUpdate
from . import repository

router = APIRouter(prefix="/pacientes/{paciente_id}/antropometrias", tags=["antropometrias"])


@router.get("/", response_model=List[AntropometriaRead])
def listar_antropometrias(paciente_id: int, db: Session = Depends(get_session)):
    return repository.list_antropometrias(db, paciente_id)


@router.post("/", response_model=AntropometriaRead, status_code=status.HTTP_201_CREATED)
def criar_antropometria(paciente_id: int, payload: AntropometriaCreate, db: Session = Depends(get_session)):
    return repository.create_antropometria(db, paciente_id, payload)


@router.get("/{antropometria_id}", response_model=AntropometriaRead)
def obter_antropometria(paciente_id: int, antropometria_id: int, db: Session = Depends(get_session)):
    antropometria = repository.get_antropometria(db, paciente_id, antropometria_id)
    if not antropometria:
        raise HTTPException(status_code=404, detail="Registro de antropometria não encontrado")
    return antropometria


@router.put("/{antropometria_id}", response_model=AntropometriaRead)
def atualizar_antropometria(paciente_id: int, antropometria_id: int, payload: AntropometriaUpdate, db: Session = Depends(get_session)):
    antropometria = repository.update_antropometria(db, paciente_id, antropometria_id, payload)
    if not antropometria:
        raise HTTPException(status_code=404, detail="Registro de antropometria não encontrado")
    return antropometria


@router.delete("/{antropometria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_antropometria(paciente_id: int, antropometria_id: int, db: Session = Depends(get_session)):
    ok = repository.delete_antropometria(db, paciente_id, antropometria_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Registro de antropometria não encontrado")
    return None
