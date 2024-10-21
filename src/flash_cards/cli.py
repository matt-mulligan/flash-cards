"""Module holding PyApp CLI entrypoint.

Logic to be kept to a minimum in this module and call out to other modules.
"""

from pathlib import Path
from typing import Optional

from pyapp.app import CliApplication, argument

from flash_cards.default_settings import AppSettings
from flash_cards.engine.console import ConsoleGameEngine
from flash_cards.io import add_question_sets_to_store

app = CliApplication(
    description="Flash Cards",
)
cli_main = app.dispatch


@app.command
def play(
    *,
    question_store_path: Optional[Path] = argument(  # noqa: B008
        "--question-store-path",
        help_text="Path to flash cards question sets file. If not given then default path will be used",
    ),
    game_store_path: Optional[Path] = argument(  # noqa: B008
        "--game-store-path",
        help_text="Path to flash cards games file. If not given then default path will be used",
    ),
):
    """Provide a greeting."""
    question_store_path = question_store_path or AppSettings.QUESTION_STORE_PATH
    game_store_path = game_store_path or AppSettings.GAME_STORE_PATH
    game = ConsoleGameEngine(question_store_path, game_store_path)
    game.play()


@app.command
def revise(
    *,
    question_store_path: Optional[Path] = argument(  # noqa: B008
        "--question-store-path",
        help_text="Path to flash cards question sets file. If not given then default path will be used",
    ),
    game_store_path: Optional[Path] = argument(  # noqa: B008
        "--game-store-path",
        help_text="Path to flash cards games file. If not given then default path will be used",
    ),
):
    """Get feedback on the questions you struggle with."""
    question_store_path = question_store_path or AppSettings.QUESTION_STORE_PATH
    game_store_path = game_store_path or AppSettings.GAME_STORE_PATH
    game = ConsoleGameEngine(question_store_path, game_store_path)
    game.revise()


@app.command(name="add-questions")
def add_questions(
    *,
    json_path: Optional[Path] = argument(  # noqa: B008
        "--json-path",
        help_text="Path to JSON file containing questions to load. If not given then default file will be used",
    ),
):
    """Add questions to the game DB via json file."""
    json_path = json_path or AppSettings.SAMPLE_QUESTION_SETS
    store_path = AppSettings.QUESTION_STORE_PATH

    add_question_sets_to_store(store_path, json_path)
