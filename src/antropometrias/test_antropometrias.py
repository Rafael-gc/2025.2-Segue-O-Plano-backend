from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, Paciente
from antropometrias import repository
from antropometrias.schema import AntropometriaCreate, AntropometriaUpdate


def test_crud_antropometria():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # criar paciente para associar antropometrias
        paciente = Paciente(nome="Paciente Antro Teste")
        db.add(paciente)
        db.commit()
        db.refresh(paciente)

        # CREATE
        payload = AntropometriaCreate(
            data=date(2025, 1, 1),
            peso_atual=70.5,
            peso_habitual=72.0,
            dobra_triceps=10.0,
            dobra_biceps=8.0,
            dobra_subescapular=12.0,
            dobra_suprailiaca=11.0,
            circunferencia_braco=30.0,
            circunferencia_cintura=85.0,
            circunferencia_abdomen=90.0,
            circunferencia_quadril=95.0,
            circunferencia_panturrilha=36.0,
            observacoes="Teste inicial"
        )
        a = repository.create_antropometria(db, paciente.id, payload)
        assert a.id is not None
        assert a.paciente_id == paciente.id
        assert abs(a.peso_atual - 70.5) < 1e-6

        # LIST
        lst = repository.list_antropometrias(db, paciente.id)
        assert any(item.id == a.id for item in lst)

        # GET
        got = repository.get_antropometria(db, paciente.id, a.id)
        assert got is not None
        assert got.observacoes == "Teste inicial"

        # UPDATE
        upd = AntropometriaUpdate(peso_atual=68.0, observacoes="Atualizado")
        updated = repository.update_antropometria(db, paciente.id, a.id, upd)
        assert updated is not None
        assert abs(updated.peso_atual - 68.0) < 1e-6
        assert updated.observacoes == "Atualizado"

        # DELETE
        ok = repository.delete_antropometria(db, paciente.id, a.id)
        assert ok is True
        assert repository.get_antropometria(db, paciente.id, a.id) is None

    finally:
        db.close()