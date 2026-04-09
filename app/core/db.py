from sqlmodel import create_engine, Session, SQLModel
from typing import Iterator

from app.core.config import settings


engine = create_engine(settings.USUARIO_DATABASE_URL, echo=False, connect_args={"check_same_thread": False} if "sqlite" in settings.USUARIO_DATABASE_URL else {})


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session