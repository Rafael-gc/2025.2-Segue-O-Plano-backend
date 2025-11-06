from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from . import repository
from .schema import AlimentoCreate, AlimentoRead, AlimentoUpdate

router = APIRouter(prefix="/alimentos", tags=["alimentos"])

# CRUD Alimentos
@router.get("/", response_model=List[AlimentoRead])
def listar_alimentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    return repository.list_alimentos(db, skip=skip, limit=limit)

@router.post("/", response_model=AlimentoRead, status_code=status.HTTP_201_CREATED)
def criar_alimento(payload: AlimentoCreate, db: Session = Depends(get_session)):
    return repository.create_alimento(db, payload)

@router.get("/{alimento_id}", response_model=AlimentoRead)
def obter_alimento(alimento_id: int, db: Session = Depends(get_session)):
    a = repository.get_alimento(db, alimento_id)
    if not a:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return a

@router.put("/{alimento_id}", response_model=AlimentoRead)
def atualizar_alimento(alimento_id: int, payload: AlimentoUpdate, db: Session = Depends(get_session)):
    a = repository.update_alimento(db, alimento_id, payload)
    if not a:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return a

@router.delete("/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_alimento(alimento_id: int, db: Session = Depends(get_session)):
    ok = repository.delete_alimento(db, alimento_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return None
