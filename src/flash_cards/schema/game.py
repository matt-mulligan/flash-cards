"""Game schemas."""

from datetime import datetime

import odin

from .base import BaseSchema
from .questions import Question


class Response(BaseSchema):
    """A players response to a question."""

    question: Question = odin.Options(doc_text="the question object for the response")
    player_answer: str = odin.Options(doc_text="the answer the player gave")

    @property
    def is_correct(self) -> bool:
        """Checks if the player answer is correct."""
        return self.question.check_answer(self.player_answer)


class Game(BaseSchema):
    """Completed game of flash cards."""

    player: str = odin.Options(doc_text="Player name")
    question_set_id: str = odin.Options(doc_text="Question set ID")
    categories: str = odin.Options(doc_text="Categories")
    question_set: str = odin.Options(doc_text="Question set being played")
    start_ts: datetime = odin.Options(doc_text="The datetime value for when the game started.")
    end_ts: datetime = odin.Options(doc_text="The datetime value for when the game ended.")
    responses: list[Response] = odin.Options(doc_text="Correct questions")

    @property
    def score(self) -> int:
        """Builds a score for the game so far, three points for a correct answer, zero for a wrong answer."""
        return sum([3 if response.is_correct else 0 for response in self.responses])

    @property
    def max_score(self) -> int:
        """Builds the max score possible."""
        return len(self.responses) * 3


class FlashCardGames(BaseSchema):
    """collection object for flash card games."""

    games: list[Game] = odin.Options(doc_text="list of completed games")
