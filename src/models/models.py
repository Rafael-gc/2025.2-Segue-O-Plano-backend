# src/models/models.py
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Time, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# ---------- TABELA ASSOCIATIVA ----------
refeicao_alimento_table = Table(
    "refeicao_alimento",
    Base.metadata,
    Column("refeicao_id", Integer, ForeignKey("refeicao.id"), primary_key=True),
    Column("alimento_id", Integer, ForeignKey("alimento.id"), primary_key=True),
    Column("quantidade", Float),
    Column("medida", String(50)),
)

# ---------- PACIENTE e ANTROPOMETRIA ----------
class Paciente(Base):
    __tablename__ = "paciente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    sexo = Column(String, nullable=True)
    gestante = Column(Boolean, nullable=True)
    altura = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    planos = relationship("Plano", back_populates="paciente")
    antropometrias = relationship("Antropometria", back_populates="paciente")

class Antropometria(Base):
    __tablename__ = "antropometria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("paciente.id"), nullable=False)

    data = Column(Date, nullable=True)
    peso_atual = Column(Float, nullable=True)
    peso_habitual = Column(Float, nullable=True)
    dobra_triceps = Column(Float, nullable=True)
    dobra_biceps = Column(Float, nullable=True)
    dobra_subescapular = Column(Float, nullable=True)
    dobra_suprailiaca = Column(Float, nullable=True)
    circunferencia_braco = Column(Float, nullable=True)
    circunferencia_cintura = Column(Float, nullable=True)
    circunferencia_abdomen = Column(Float, nullable=True)
    circunferencia_quadril = Column(Float, nullable=True)
    circunferencia_panturrilha = Column(Float, nullable=True)
    observacoes = Column(String, nullable=True)

    paciente = relationship("Paciente", back_populates="antropometrias")


# ---------- PLANO e REFEICAO ----------
class Plano(Base):
    __tablename__ = "plano"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("paciente.id"), nullable=False)

    data_inicio = Column(Date, nullable=True)
    data_fim = Column(Date, nullable=True)
    objetivo = Column(String, nullable=True)

    paciente = relationship("Paciente", back_populates="planos")
    refeicoes = relationship("Refeicao", back_populates="plano")


class Refeicao(Base):
    __tablename__ = "refeicao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plano_id = Column(Integer, ForeignKey("plano.id"), nullable=False)
    horario = Column(Time, nullable=True)
    descricao = Column(String, nullable=True)

    plano = relationship("Plano", back_populates="refeicoes")
    alimentos = relationship("Alimento", secondary=refeicao_alimento_table, back_populates="refeicoes")


# ---------- ALIMENTO ----------
class Alimento(Base):
    __tablename__ = "alimento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    kcal = Column(Float, nullable=True)
    proteinas = Column(Float, nullable=True)
    carboidratos = Column(Float, nullable=True)
    lipideos = Column(Float, nullable=True)

    refeicoes = relationship("Refeicao", secondary=refeicao_alimento_table, back_populates="alimentos")
