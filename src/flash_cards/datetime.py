"""Module to handle datetime generation and conversion.

ensures that all datetimes are aware (contain timezone info)
"""

from datetime import datetime

import arrow

from .exceptions import NaiveDatetime


def get_current_datetime(local: bool = True) -> datetime:
    """Build aware datetime object for current timestamp with either local or UTC timezone."""
    return arrow.now().datetime if local else arrow.utcnow().datetime


def to_utc(dt: datetime) -> datetime:
    """Convert timestamp object to be UTC timezone."""
    if not dt.tzinfo:
        raise NaiveDatetime()

    return arrow.get(dt).to("utc").datetime


def to_local(dt: datetime) -> datetime:
    """Convert timestamp object to be local timezone."""
    if not dt.tzinfo:
        raise NaiveDatetime()

    return arrow.get(dt).to("local").datetime
