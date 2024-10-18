"""Module to hold game engine implementations."""

import datetime
import random
from abc import ABC, abstractmethod
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from flash_cards.constants import ASCII_ART
from flash_cards.io import add_game_to_store, load_question_sets
from flash_cards.schema.game import Game, Response
from flash_cards.schema.questions import FreeTextQuestion, MultiChoiceQuestion


class GameEngine(ABC):
    """Base game engine class."""

    def __init__(self, question_store_path: Path, game_store_path: Path):
        """Create instance of class."""
        self.console = Console(width=280)
        self.question_store_path = question_store_path
        self.game_store_path = game_store_path
        self.question_sets = load_question_sets(question_store_path)
        self.questions = None
        self.game = Game(start_ts=datetime.datetime.now())

    def play(self):
        """Run main game loop."""
        self.startup_graphics()
        self.game.player = self.get_player()
        self.game.categories, self.game.question_set, self.game.question_set_id = self.get_question_set_info()
        self.questions = self.question_sets.get_question_set_by_id(self.game.question_set_id).questions
        random.shuffle(self.questions)

        for q_num, question in enumerate(self.questions, start=1):
            self.game.responses.append(self.get_player_response(q_num, question))

        self.game.end_ts = datetime.datetime.now()
        self.report_final_result(self.game)
        add_game_to_store(self.game_store_path, self.game)

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


class ConsoleGameEngine(GameEngine):
    """rich enabled console game engine."""

    def startup_graphics(self):
        """Display console startup graphics."""
        self.console.print(Panel.fit(f"[green]{ASCII_ART}", border_style="blue"))

    def get_player(self) -> str:
        """Abstract method to get the player name."""
        self.console.print(Panel.fit("[bold yellow]Player Info", border_style="red"))
        name = self.console.input("\n:question_mark: What is your name: ")
        self.console.print(f"\nWelcome {name}! Lets Play!\n")
        return name

    def get_question_set_info(self) -> tuple[list[str], str, str]:
        """Ask user which question set to load."""
        unique_categories = self.question_sets.unique_categories

        self.console.print(Panel.fit("[bold yellow]Category Selection", border_style="red"))

        previous_selections = []
        while True:
            selected_amount = len(previous_selections)
            possible_categories = [cat for cat in unique_categories if cat[:selected_amount] == previous_selections]

            if len(possible_categories) == 1:
                break

            options = {cats[selected_amount] for cats in possible_categories}
            if selected_amount > 0:
                prompt = (
                    f"\n:question_mark: Given the selected categories of {', '.join(previous_selections)}, "
                    f"which sub-category would you like to play?"
                )
            else:
                prompt = "\n:question_mark: Which category would you like to play?"

            previous_selections.append(self.ask_multi_choice_question(prompt, options))

        categories = possible_categories[0]
        possible_names = self.question_sets.get_set_names_for_category(categories)
        set_name = self.ask_multi_choice_question(
            (
                f"\n:question_mark: Which question set from category {' -> '.join(categories)} "
                f"would you like to play?"
            ),
            possible_names,
        )

        set_id = self.question_sets.get_question_set_by_components(categories, set_name).id

        return categories, set_name, set_id

    def ask_multi_choice_question(self, prompt, options) -> str:
        """Ask multi-choice question with checks."""
        while True:
            question_text = "\n".join([prompt, *[f"\t{option}" for option in options]])
            question_text = f"{question_text}\n"
            player_answer = self.console.input(question_text)

            if player_answer not in options:
                self.console.print("That's not a valid answer! Try again!")
                continue

            return player_answer

    def get_player_response(self, q_num: int, question: FreeTextQuestion | MultiChoiceQuestion) -> Response:
        """Ask a player the question and get their response."""
        self.console.print(f"\nQuestion {q_num} of {len(self.questions)}:")

        if isinstance(question, MultiChoiceQuestion):
            player_answer = self.ask_multi_choice_question(f":question_mark: {question.prompt}\n", question.choices)
        else:
            player_answer = self.console.input(f":question_mark: {question.prompt}\n")

        return Response(question, player_answer)

    def report_final_result(self, game: Game):
        """Report the final result."""
        correct = [resp for resp in game.responses if resp.is_correct]
        incorrect = [resp for resp in game.responses if not resp.is_correct]

        self.console.print("\n:checkered_flag: FINAL RESULTS!! :checkered_flag:")
        self.console.print(f"\t:man_dancing: Player: {game.player}")
        self.console.print(f"\t:question_mark: Question Categories: {' -> '.join(game.categories)}\n")

        self.console.print("\tCorrect Results:")
        for resp in correct:
            self.console.print(f"\t\t✅{resp.question.prompt}\t ANSWER: {resp.player_answer}")

        self.console.print("\n\tIncorrect Results:")
        for resp in incorrect:
            self.console.print(
                f"\t\t❌{resp.question.prompt}\tPLAYER: {resp.player_answer}\tACTUAL: {resp.question.answer}"
            )

        self.console.print(f"\n\tResult: {game.score} out of {game.max_score}!")
        self.console.print(f"\tWell Done {game.player}! Keep playing!")
