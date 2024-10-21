"""Handle IO."""

from pathlib import Path

from odin.codecs import json_codec

from flash_cards.schema.game import FlashCardGames, Game
from flash_cards.schema.questions import QuestionSets


def load_question_sets(store_path: Path) -> QuestionSets:
    """Load question set from file."""
    with store_path.open(mode="r") as json_file:
        return json_codec.load(json_file, QuestionSets)


def load_games(store_path: Path) -> FlashCardGames:
    """Load games from file."""
    with store_path.open(mode="r") as json_file:
        return json_codec.load(json_file, FlashCardGames)


def dump_question_sets(store_path: Path, question_sets: QuestionSets):
    """Dump question sets to file."""
    store_path.parent.mkdir(parents=True, exist_ok=True)

    with store_path.open(mode="w") as json_file:
        return json_codec.dump(question_sets, json_file)


def dump_games(store_path: Path, games: FlashCardGames):
    """Dump games to file."""
    store_path.parent.mkdir(parents=True, exist_ok=True)

    with store_path.open(mode="w") as json_file:
        return json_codec.dump(games, json_file)


def merge_question_sets(existing: QuestionSets, new: QuestionSets) -> QuestionSets:
    """Merge question sets."""
    for new_qs in new.question_sets:
        existing_qs_matches = [ex_qs for ex_qs in existing.question_sets if ex_qs.id == new_qs.id]
        if not existing_qs_matches:
            existing.question_sets.append(new_qs)
            continue

        existing_qs = existing_qs_matches[0]
        for question in new_qs.questions:
            existing_qs.questions = [ex_quest for ex_quest in existing_qs.questions if ex_quest.id != question.id]
            existing_qs.questions.append(question)

    return existing


def add_question_sets_to_store(store_path: Path, question_sets_path: Path):
    """Add new question sets to store."""
    existing_question_sets = load_question_sets(store_path) if store_path.exists() else QuestionSets()
    new_question_sets = load_question_sets(question_sets_path)
    updated_question_sets = merge_question_sets(existing_question_sets, new_question_sets)
    dump_question_sets(store_path, updated_question_sets)


def add_game_to_store(store_path: Path, game: Game):
    """Add new game to store."""
    game.full_clean()

    games = load_games(store_path) if store_path.exists() else FlashCardGames()
    games.games.append(game)
    dump_games(store_path, games)
