"""SQLAlchemy Question ORM Definition."""

from sqlalchemy.orm import Mapped, mapped_column

from flash_cards.constants import AnswerStrictness
from flash_cards.orm.base import Base


class Question(Base):
    """SQLAlchemy ORM Class for a question."""

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(doc="Unique ID of the game played", primary_key=True, autoincrement=True)
    sets: Mapped[str] = mapped_column(doc="set this question belongs to")
    prompt: Mapped[str] = mapped_column(doc="Question prompt")
    answer: Mapped[str] = mapped_column(doc="Question answer")
    strictness: Mapped[AnswerStrictness]

    def __repr__(self) -> str:
        """Representation of object."""
        return f"Question('{self.prompt}')"

    def check_response(self, response: str) -> tuple[bool, str]:
        """Check response against answer."""
        if self.strictness == AnswerStrictness.Strict:
            return response == self.answer, self.answer

        return response.casefold() == self.answer.casefold(), self.answer
