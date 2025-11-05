from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from database import get_session
from . import repository as refeicoes_repo
from .schema import RefeicaoCreate, RefeicaoRead, RefeicaoUpdate

# import das funções/ schemas da camada de alimentos (associação)
from alimentos import repository as alimentos_repo
from alimentos.schema import RefeicaoAlimentoCreate, RefeicaoAlimentoRead

router = APIRouter(prefix="/pacientes/{paciente_id}/planos/{plano_id}/refeicoes", tags=["refeicoes"])


@router.get("/", response_model=List[RefeicaoRead])
def listar_refeicoes(paciente_id: int, plano_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    try:
        return refeicoes_repo.list_refeicoes(db, paciente_id, plano_id, skip=skip, limit=limit)
    except ValueError:
        raise HTTPException(status_code=404, detail="Plano não encontrado")


@router.post("/", response_model=RefeicaoRead, status_code=status.HTTP_201_CREATED)
def criar_refeicao(paciente_id: int, plano_id: int, payload: RefeicaoCreate, db: Session = Depends(get_session)):
    try:
        return refeicoes_repo.create_refeicao(db, paciente_id, plano_id, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="Plano não encontrado")


@router.get("/{refeicao_id}", response_model=RefeicaoRead)
def obter_refeicao(paciente_id: int, plano_id: int, refeicao_id: int, db: Session = Depends(get_session)):
    try:
        r = refeicoes_repo.get_refeicao(db, paciente_id, plano_id, refeicao_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    if not r:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    return r


@router.put("/{refeicao_id}", response_model=RefeicaoRead)
def atualizar_refeicao(paciente_id: int, plano_id: int, refeicao_id: int, payload: RefeicaoUpdate, db: Session = Depends(get_session)):
    try:
        r = refeicoes_repo.update_refeicao(db, paciente_id, plano_id, refeicao_id, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    if not r:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    return r


@router.delete("/{refeicao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_refeicao(paciente_id: int, plano_id: int, refeicao_id: int, db: Session = Depends(get_session)):
    try:
        ok = refeicoes_repo.delete_refeicao(db, paciente_id, plano_id, refeicao_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    if not ok:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")
    return None


# ------------------ Endpoints de associação Refeição <-> Alimento ------------------

@router.post("/{refeicao_id}/alimentos", status_code=status.HTTP_201_CREATED)
def adicionar_alimento_na_refeicao(paciente_id: int, plano_id: int, refeicao_id: int, payload: RefeicaoAlimentoCreate, db: Session = Depends(get_session)):
    # valida plano/refeicao via refeicoes_repo (levanta ValueError se não pertence)
    try:
        # garante plano/refeicao válidos
        _ = refeicoes_repo.get_refeicao(db, paciente_id, plano_id, refeicao_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    try:
        return alimentos_repo.add_alimento_to_refeicao(db, refeicao_id, payload)
    except ValueError as e:
        msg = str(e)
        if "refeicao_nao_encontrada" in msg:
            raise HTTPException(status_code=404, detail="Refeição não encontrada")
        if "alimento_nao_encontrado" in msg:
            raise HTTPException(status_code=404, detail="Alimento não encontrado")
        raise HTTPException(status_code=400, detail=msg)


@router.get("/{refeicao_id}/alimentos", response_model=List[RefeicaoAlimentoRead])
def listar_alimentos_da_refeicao(paciente_id: int, plano_id: int, refeicao_id: int, db: Session = Depends(get_session)):
    try:
        # valida plano/refeicao
        _ = refeicoes_repo.get_refeicao(db, paciente_id, plano_id, refeicao_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    items = alimentos_repo.list_alimentos_da_refeicao(db, refeicao_id)
    return [{"alimento": item["alimento"], "quantidade": item["quantidade"], "medida": item["medida"]} for item in items]


@router.put("/{refeicao_id}/alimentos/{alimento_id}", response_model=RefeicaoAlimentoRead)
def atualizar_alimento_da_refeicao(paciente_id: int, plano_id: int, refeicao_id: int, alimento_id: int, payload: RefeicaoAlimentoCreate, db: Session = Depends(get_session)):
    try:
        _ = refeicoes_repo.get_refeicao(db, paciente_id, plano_id, refeicao_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    ok = alimentos_repo.update_alimento_refeicao(db, refeicao_id, alimento_id, payload.quantidade, payload.medida)
    if not ok:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    # retorna estado atual
    return {"alimento": alimentos_repo.get_alimento(db, alimento_id), "quantidade": payload.quantidade, "medida": payload.medida}


@router.delete("/{refeicao_id}/alimentos/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_alimento_da_refeicao(paciente_id: int, plano_id: int, refeicao_id: int, alimento_id: int, db: Session = Depends(get_session)):
    try:
        _ = refeicoes_repo.get_refeicao(db, paciente_id, plano_id, refeicao_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    ok = alimentos_repo.remove_alimento_from_refeicao(db, refeicao_id, alimento_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return None