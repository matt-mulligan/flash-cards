"""ORM package.

Contains all models and code define the sqlalchemy object model and interact with sqlite storage.
"""

from collections.abc import Sequence
from pathlib import Path

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session

from ..default_settings import AppSettings
from .base import Base
from .game import Game
from .question import Question


def _get_engine(db_path: Path | None = None) -> Engine:
    """Build sqlalchemy engine for game data."""
    db_path = db_path or AppSettings.DEFAULT_DB
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite+pysqlite:///{db_path}")


def create_tables(db_path: Path | None = None) -> None:
    """Create tables in sqlite DB."""
    Base.metadata.create_all(bind=_get_engine(db_path))


def get_questions(*, question_set: str | None = None, db_path: Path | None = None) -> Sequence[Question]:
    """Retrieve question set from database."""
    engine = _get_engine(db_path)

    stmt = select(Question).where(Question.sets == question_set) if question_set else select(Question)

    with Session(engine) as session:
        return session.scalars(stmt).all()


def submit_game(game_instance: Game, *, db_path: Path | None = None) -> None:
    """Add game to database."""
    with Session(_get_engine(db_path)) as session:
        session.add(game_instance)
        session.commit()
