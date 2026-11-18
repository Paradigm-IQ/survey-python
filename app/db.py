import os
from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./survey.db")

engine = create_engine(
    DATABASE_URL,
    echo=os.environ.get("SQL_ECHO") == "1",
    # Needed for SQLite when FastAPI serves requests across threads.
    connect_args={"check_same_thread": False},
)


def init_db() -> None:
    # Import models so they register with SQLModel.metadata before create_all.
    from app import models  # noqa: F401

    # No migrations: tables are created on startup. If you change a model,
    # delete survey.db (or run `make reset`-style: rm survey.db) and restart.
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
