"""Exception module."""


class FlashCardsError(Exception):
    """Base exception class for flash cards errors."""


class QuestionSetNotFound(FlashCardsError):  # noqa: N818
    """Error raised when the requested flash card question set cannot be found."""
