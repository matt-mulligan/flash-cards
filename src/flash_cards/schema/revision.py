"""Module to hold schemas for revisions."""

import odin

from .base import BaseSchema
from .game import Game, Response


class Revision(BaseSchema):
    """Revisions required for a given category/game."""

    question_set_id: str = odin.Options(doc_text="Question set ID for this revision.")
    categories: list[str] = odin.Options(doc_text="List of categories for this revision.")
    question_set: str = odin.Options(doc_text="Question set for this revision.")
    responses: list[Response] = odin.Options(doc_text="List of incorrect responses for this revision.")

    @classmethod
    def from_game(cls, game: Game) -> "Revision":
        """Build revision from game object."""
        return cls(
            question_set_id=game.question_set_id,
            categories=game.categories,
            question_set=game.question_set,
            responses=[response for response in game.responses if not response.is_correct],
        )

    def add_responses(self, responses: list[Response]):
        """Add incorrect responses for this revision."""
        self.responses.extend([response for response in responses if not response.is_correct])


class RevisionSet(BaseSchema):
    """Set of revision categories."""

    revisions: list[Revision] = odin.Options(doc_text="list of revision topics.")

    def add_games(self, games: list[Game]):
        """Add game to revision set."""
        for game in games:
            revision = [rev for rev in self.revisions if rev.question_set_id == game.question_set_id]
            if not revision:
                self.revisions.append(Revision.from_game(game))
            else:
                revision[0].add_responses(game.responses)
