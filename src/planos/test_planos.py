from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, Paciente
from planos import repository
from planos.schema import PlanoCreate, PlanoUpdate


def test_crud_plano():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # criar paciente para associar o plano
        paciente = Paciente()
        # atribua nome se o modelo tiver esse campo; se não, apenas persista para obter id
        try:
            paciente.nome = "Paciente Plano Teste"
        except Exception:
            pass
        db.add(paciente)
        db.commit()
        db.refresh(paciente)

        # CREATE
        payload = PlanoCreate(
            data_inicio=date(2025, 1, 1),
            data_fim=date(2025, 2, 1),
            objetivo="Perda de peso"
        )
        plano = repository.create_plano(db, paciente.id, payload)
        assert plano.id is not None
        assert plano.paciente_id == paciente.id

        # LIST
        lst = repository.list_planos(db, paciente.id)
        assert any(item.id == plano.id for item in lst)

        # GET
        got = repository.get_plano(db, paciente.id, plano.id)
        assert got is not None
        assert got.objetivo == "Perda de peso"

        # UPDATE
        upd = PlanoUpdate(objetivo="Ganho de massa")
        updated = repository.update_plano(db, paciente.id, plano.id, upd)
        assert updated is not None
        assert updated.objetivo == "Ganho de massa"

        # DELETE
        ok = repository.delete_plano(db, paciente.id, plano.id)
        assert ok is True
        assert repository.get_plano(db, paciente.id, plano.id) is None

    finally:
        db.close()