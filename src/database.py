import os
import time
import logging
from typing import Generator

from sqlmodel import SQLModel, create_engine, Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://segueoplano_user:segueoplano_pass@db:3306/segueoplano_db",
)

# engine com pool_pre_ping para conexões estáveis
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)


def wait_for_db(max_retries: int = 30, delay: float = 1.0) -> None:
    attempts = 0
    while attempts < max_retries:
        try:
            with engine.connect() as conn:
                logger.info("Conectado ao banco de dados.")
                return
        except Exception as exc:
            attempts += 1
            logger.info("MySQL não disponível (tentativa %d/%d): %s — aguardando %.1fs", attempts, max_retries, exc, delay)
            time.sleep(delay)
            delay = min(delay * 1.5, 10.0)
    raise RuntimeError("Não foi possível conectar ao banco após várias tentativas.")


def init_db() -> None:
    wait_for_db()
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()