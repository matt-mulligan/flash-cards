"""Module to hold game engine implementations."""

import datetime
import random
from abc import ABC, abstractmethod
from pathlib import Path

from rich.console import Console

from flash_cards.datetime import get_current_datetime
from flash_cards.io import add_game_to_store, load_games, load_question_sets
from flash_cards.schema.game import Game, Response
from flash_cards.schema.questions import FreeTextQuestion, MultiChoiceQuestion
from flash_cards.schema.revision import RevisionSet


class GameEngine(ABC):
    """Base game engine class."""

    def __init__(self, question_store_path: Path, game_store_path: Path):
        """Create instance of class."""
        self.console = Console(width=280)
        self.question_store_path = question_store_path
        self.game_store_path = game_store_path
        self.question_sets = load_question_sets(question_store_path)
        self.questions = None
        self.game = Game(start_dt=get_current_datetime())

    def play(self):
        """Run main game loop."""
        self.startup_graphics()
        self.game.player = self.get_player()
        self.game.categories, self.game.question_set, self.game.question_set_id = self.get_question_set_info()
        self.questions = self.question_sets.get_question_set_by_id(self.game.question_set_id).questions
        random.shuffle(self.questions)

        for q_num, question in enumerate(self.questions, start=1):
            self.game.responses.append(self.get_player_response(q_num, question))

        self.game.end_dt = get_current_datetime()
        self.report_final_result(self.game)
        add_game_to_store(self.game_store_path, self.game)

    def revise(self):
        """Run a revision cycle."""
        self.startup_graphics()
        self.game.player = self.get_player()

        games = load_games(self.game_store_path)
        player_games = games.find_player_games(self.game.player)
        total_played = len(player_games)

        cutoff_ts = get_current_datetime() - datetime.timedelta(days=7)
        player_games = [game for game in player_games if game.start_dt_local > cutoff_ts]
        played_in_cutoff = len(player_games)

        rev_set = RevisionSet()
        rev_set.add_games(player_games)
        self.report_revisions(total_played, played_in_cutoff, rev_set)

    @abstractmethod
    def startup_graphics(self) -> str:
        """Abstract method to display startup graphics for the game."""

    @abstractmethod
    def get_player(self) -> str:
        """Abstract method to get the player name."""

    @abstractmethod
    def get_question_set_info(self) -> tuple[list[str], str, str]:
        """Abstract method to get the question set from the player."""

    @abstractmethod
    def get_player_response(self, q_num: int, question: FreeTextQuestion | MultiChoiceQuestion) -> Response:
        """Abstract method to ask a player the question and check if it's right."""

    @abstractmethod
    def report_final_result(self, game: Game):
        """Abstract method to report the final result."""

    @abstractmethod
    def report_revisions(self, total_played: int, played_in_cutoff: int, rev_set: RevisionSet):
        """Abstract method to report revisions."""
