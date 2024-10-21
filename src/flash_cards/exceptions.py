"""Exception module."""


class FlashCardsError(Exception):
    """Base exception class for flash cards errors."""


class NaiveDatetime(FlashCardsError):  # noqa: N818
    """Error raised when using naive datetimes.

    Datetime should always be aware (have timezone information) and always stored as UTC
    """


class QuestionSetNotFound(FlashCardsError):  # noqa: N818
    """Error raised when the requested flash card question set cannot be found."""
