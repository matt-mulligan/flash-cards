"""Constants."""

from enum import Enum


class AnswerStrictness(Enum):
    """Defines the strictness of the answer."""

    Strict = "strict"
    CaseInsensitive = "case-insensitive"


DEFAULT_CATEGORY_SECONDARY = "NO_SECONDARY_CATEGORY"
DEFAULT_CATEGORY_TERTIARY = "NO_TERTIARY_CATEGORY"


ASCII_ART = r"""
    ________           __       ______               __     __
   / ____/ /___ ______/ /_     / ____/___ __________/ /____/ /
  / /_  / / __ `/ ___/ __ \   / /   / __ `/ ___/ __  / ___/ / 
 / __/ / / /_/ (__  ) / / /  / /___/ /_/ / /  / /_/ (__  )_/  
/_/   /_/\__,_/____/_/ /_/   \____/\__,_/_/   \__,_/____(_)   
"""  # noqa: W291
