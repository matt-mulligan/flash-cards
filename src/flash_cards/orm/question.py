"""SQLAlchemy Question ORM Definition."""

from sqlalchemy.orm import Mapped, mapped_column

from flash_cards.constants import AnswerStrictness
from flash_cards.orm.base import Base


class Question(Base):
    """SQLAlchemy ORM Class for a question."""

    __tablename__ = "question"

    # id: Mapped[int] = mapped_column(doc="Unique ID of the question", primary_key=True)
    sets: Mapped[list[str]] = mapped_column(doc="List of question sets this question belongs to")
    prompt: Mapped[str] = mapped_column(doc="Question prompt")
    answer: Mapped[str] = mapped_column(doc="Question answer")
    strictness: Mapped[AnswerStrictness]

    def check_response(self, response: str) -> tuple[bool, str]:
        """Check response against answer."""
        if self.strictness == AnswerStrictness.Strict:
            return response == self.answer, self.answer

        return response.casefold() == self.answer.casefold(), self.answer
