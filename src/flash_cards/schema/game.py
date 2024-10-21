"""Game schemas."""

from datetime import datetime

import arrow
import odin
from odin.exceptions import ValidationError

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
    categories: list[str] = odin.Options(doc_text="Categories")
    question_set: str = odin.Options(doc_text="Question set being played")
    start_dt: datetime = odin.Options(doc_text="The datetime value for when the game started in UTC.")
    end_dt: datetime = odin.Options(doc_text="The datetime value for when the game ended in UTC.")
    responses: list[Response] = odin.Options(doc_text="Correct questions")

    @staticmethod
    def clean_start_dt(value: datetime) -> datetime:
        """Ensure start_dt is always an aware datetime in UTC."""
        if not value.tzinfo:
            raise ValidationError("start_dt must be an aware datetime")

        return arrow.get(value).to("utc").datetime

    @staticmethod
    def clean_end_dt(value: datetime) -> datetime:
        """Ensure start_dt is always an aware datetime in UTC."""
        if not value.tzinfo:
            raise ValidationError("end_dt must be an aware datetime")

        return arrow.get(value).to("utc").datetime

    @property
    def start_dt_local(self) -> datetime:
        """Returns the start_dt value for the current timezone."""
        return arrow.get(self.start_dt).to("local").datetime

    @property
    def end_dt_local(self) -> datetime:
        """Returns the start_dt value for the current timezone."""
        return arrow.get(self.end_dt).to("local").datetime

    @property
    def score(self) -> int:
        """Builds a score for the game so far, three points for a correct answer, zero for a wrong answer."""
        return sum([3 if response.is_correct else 0 for response in self.responses])

    @property
    def max_score(self) -> int:
        """Builds the max score possible."""
        return len(self.responses) * 3

    @property
    def correct_responses(self) -> list[Response]:
        """Get list of correct responses."""
        return [resp for resp in self.responses if resp.is_correct]

    @property
    def incorrect_responses(self) -> list[Response]:
        """Get list of incorrect responses."""
        return [resp for resp in self.responses if resp.is_correct]


class FlashCardGames(BaseSchema):
    """collection object for flash card games."""

    games: list[Game] = odin.Options(doc_text="list of completed games")

    def find_player_games(self, player: str) -> list[Game]:
        """Get list of games for given player."""
        return [game for game in self.games if game.player == player]
