"""Constants."""

from enum import Enum


class AnswerStrictness(Enum):
    """Defines the strictness of the answer."""

    Strict = "strict"
    CaseInsensitive = "case-insensitive"
