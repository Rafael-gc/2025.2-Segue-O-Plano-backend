from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base
from pacientes import repository
from pacientes.schema import PacienteCreate, PacienteUpdate


def test_crud_paciente():
    # usa SQLite in-memory para os testes (isolado, rápido)
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # CREATE
        payload = PacienteCreate(
            nome="Paciente Teste",
            email="teste@example.com",
            telefone="11999999999",
            data_nascimento=date(1990, 1, 1),
            sexo="masculino",
            gestante=False,
            altura=1.75,
        )
        p = repository.create_paciente(db, payload)
        assert p.id is not None
        assert p.nome == "Paciente Teste"

        # LIST
        lst = repository.list_pacientes(db)
        assert any(item.id == p.id for item in lst)

        # GET
        got = repository.get_paciente(db, p.id)
        assert got is not None
        assert got.email == "teste@example.com"

        # UPDATE
        upd = PacienteUpdate(telefone="11988888888")
        updated = repository.update_paciente(db, p.id, upd)
        assert updated is not None
        assert updated.telefone == "11988888888"

        # DELETE
        ok = repository.delete_paciente(db, p.id)
        assert ok is True
        assert repository.get_paciente(db, p.id) is None

    finally:
        db.close()