"""Default settings file for flash cards app."""

from pathlib import Path

from pyapp.typed_settings import SettingsDef


class AppSettings(SettingsDef):
    """Defines the default settings for flash cards app."""

    DEFAULT_DB: Path = Path.home() / "flash_cards" / "data" / "flash_cards.sqlite"
