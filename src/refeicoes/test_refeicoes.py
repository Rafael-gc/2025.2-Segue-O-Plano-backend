from datetime import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, Paciente, Plano
from refeicoes import repository
from refeicoes.schema import RefeicaoCreate, RefeicaoUpdate


def test_crud_refeicao():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # criar paciente e plano para associar a refeição
        paciente = Paciente()
        try:
            paciente.nome = "Paciente Refeicao Teste"
        except Exception:
            pass
        db.add(paciente)
        db.commit()
        db.refresh(paciente)

        plano = Plano(paciente_id=paciente.id)
        db.add(plano)
        db.commit()
        db.refresh(plano)

        # CREATE
        payload = RefeicaoCreate(horario=time(12, 0), descricao="Almoço teste")
        r = repository.create_refeicao(db, paciente.id, plano.id, payload)
        assert r.id is not None
        assert r.plano_id == plano.id
        assert r.descricao == "Almoço teste"

        # LIST
        lst = repository.list_refeicoes(db, paciente.id, plano.id)
        assert any(item.id == r.id for item in lst)

        # GET
        got = repository.get_refeicao(db, paciente.id, plano.id, r.id)
        assert got is not None
        assert got.descricao == "Almoço teste"

        # UPDATE
        upd = RefeicaoUpdate(descricao="Almoço atualizado")
        updated = repository.update_refeicao(db, paciente.id, plano.id, r.id, upd)
        assert updated is not None
        assert updated.descricao == "Almoço atualizado"

        # DELETE
        ok = repository.delete_refeicao(db, paciente.id, plano.id, r.id)
        assert ok is True
        assert repository.get_refeicao(db, paciente.id, plano.id, r.id) is None

    finally:
        db.close()