"""Question schemas."""

import hashlib
import random
from abc import abstractmethod

import odin

from flash_cards.constants import AnswerStrictness

from ..exceptions import QuestionSetNotFound
from .base import BaseSchema


class Question(BaseSchema, abstract=True):
    """abstract question."""

    prompt: str = odin.Options(doc_text="the question prompt to present the player")
    answer: str = odin.Options(doc_text="the question answer")

    @property
    def id(self) -> str:
        """Generate question ID."""
        return hashlib.md5(self.prompt.encode("utf-8")).hexdigest()  # noqa: S324

    @abstractmethod
    def check_answer(self, response: str) -> bool:
        """Check response and returns bool indicating if correct."""


class FreeTextQuestion(Question):
    """free text questions."""

    strictness: AnswerStrictness = odin.Options(doc_text="the answer strictness to present the player")

    def check_answer(self, response: str) -> bool:
        """Check response and returns bool indicating if correct."""
        if self.strictness == AnswerStrictness.Strict:
            return self.answer == response

        return self.answer.casefold() == response.casefold()


class MultiChoiceQuestion(Question):
    """multi choice questions."""

    incorrect_answers: list[str] = odin.Options(doc_text="list of incorrect answers to provide to the player")

    @property
    def choices(self) -> list[str]:
        """Build choices list."""
        choices = [self.answer, *self.incorrect_answers]
        random.shuffle(choices)
        return choices

    def check_answer(self, response: str) -> bool:
        """Check response and returns bool indicating if correct."""
        return response == self.answer


class QuestionSet(BaseSchema):
    """Individual question set."""

    name: str = odin.Options(doc_text="name of the question set")
    categories: list[str] = odin.Options(doc_text="ordered list of categories for the question set")
    questions: list[Question] = odin.Options(doc_text="list of questions for the question set.")

    @property
    def id(self) -> str:
        """Build question set ID."""
        return hashlib.md5(".".join([*self.categories, self.name]).encode("utf-8")).hexdigest()  # noqa: S324


class QuestionSets(BaseSchema):
    """collection of question sets."""

    question_sets: list[QuestionSet] = odin.Options(doc_text="List of question sets known to the app")

    @property
    def unique_categories(self) -> list[list[str]]:
        """Get a list of all unique categories for question sets."""
        cat_list = []
        for question_set in self.question_sets:
            if question_set.categories not in cat_list:
                cat_list.append(question_set.categories)

        return cat_list

    def get_question_set_by_components(self, categories: list[str], name: str) -> QuestionSet:
        """Get question set by components."""
        sets = [qs for qs in self.question_sets if qs.categories == categories and qs.name == name]
        if not sets:
            raise QuestionSetNotFound(f"No question set matching categories {categories} and name {name} was found.")

        return sets[0]

    def get_question_set_by_id(self, id: str) -> QuestionSet:
        """Get question set by id."""
        sets = [qs for qs in self.question_sets if qs.id == id]
        if not sets:
            raise QuestionSetNotFound(f"No question set matching ID {id} was found.")

        return sets[0]

    def get_set_names_for_category(self, categories: list[str]) -> list[str]:
        """Get list of names of question sets for category."""
        return [qs.name for qs in self.question_sets if qs.categories == categories]
