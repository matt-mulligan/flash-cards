"""SQLAlchemy Game ORM Definition."""

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from flash_cards.orm.base import Base


class Game(Base):
    """SQLAlchemy ORM Class for a game."""

    __tablename__ = "game"

    id: Mapped[int] = mapped_column(doc="Unique ID of the game played", primary_key=True)
    player: Mapped[str] = mapped_column(doc="name of the player")
    set: Mapped[str] = mapped_column(doc="set of questions for the game")
    timestamp: Mapped[datetime] = mapped_column(doc="datetime when the game was played")
    attempted: Mapped[int] = mapped_column(doc="number of questions attempted")
    correct: Mapped[int] = mapped_column(doc="number of questions correctly answered")
