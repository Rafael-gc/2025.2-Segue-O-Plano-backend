from datetime import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, Paciente, Plano, Refeicao
from alimentos import repository
from alimentos.schema import AlimentoCreate, AlimentoUpdate, RefeicaoAlimentoCreate


def test_crud_e_associacao_alimento():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # criar paciente, plano e refeição para associação
        paciente = Paciente()
        try:
            paciente.nome = "Paciente Alimento Teste"
        except Exception:
            pass
        db.add(paciente)
        db.commit()
        db.refresh(paciente)

        plano = Plano(paciente_id=paciente.id)
        db.add(plano)
        db.commit()
        db.refresh(plano)

        refeicao = Refeicao(plano_id=plano.id, horario=time(12, 0), descricao="Almoço teste")
        db.add(refeicao)
        db.commit()
        db.refresh(refeicao)

        # CREATE alimento
        payload = AlimentoCreate(
            nome="Banana",
            descricao="Banana prata",
            kcal=89,
            proteinas=1.1,
            carboidratos=22.8,
            lipideos=0.3
        )
        a = repository.create_alimento(db, payload)
        assert a.id is not None
        assert a.nome == "Banana"

        # LIST
        lst = repository.list_alimentos(db)
        assert any(item.id == a.id for item in lst)

        # GET
        got = repository.get_alimento(db, a.id)
        assert got is not None
        assert got.kcal == 89

        # UPDATE
        upd = AlimentoUpdate(nome="Banana Atualizada", kcal=95)
        updated = repository.update_alimento(db, a.id, upd)
        assert updated is not None
        assert updated.nome == "Banana Atualizada"
        assert updated.kcal == 95

        # ASSOCIAR alimento à refeição
        assoc_payload = RefeicaoAlimentoCreate(alimento_id=a.id, quantidade=100.0, medida="g")
        assoc = repository.add_alimento_to_refeicao(db, refeicao.id, assoc_payload)
        assert assoc["refeicao_id"] == refeicao.id
        assert assoc["alimento_id"] == a.id

        # LISTAR alimentos da refeição
        itens = repository.list_alimentos_da_refeicao(db, refeicao.id)
        assert any(item["alimento"].id == a.id and item["quantidade"] == 100.0 for item in itens)

        # ATUALIZAR associação
        ok = repository.update_alimento_refeicao(db, refeicao.id, a.id, 150.0, "g")
        assert ok is True
        itens2 = repository.list_alimentos_da_refeicao(db, refeicao.id)
        assert any(item["alimento"].id == a.id and item["quantidade"] == 150.0 for item in itens2)

        # REMOVER associação
        ok_rm = repository.remove_alimento_from_refeicao(db, refeicao.id, a.id)
        assert ok_rm is True
        itens3 = repository.list_alimentos_da_refeicao(db, refeicao.id)
        assert all(item["alimento"].id != a.id for item in itens3)

        # DELETE alimento
        ok_del = repository.delete_alimento(db, a.id)
        assert ok_del is True
        assert repository.get_alimento(db, a.id) is None

    finally:
        db.close()