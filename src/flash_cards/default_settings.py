"""Default settings file for flash cards app."""

from pathlib import Path

from pyapp.typed_settings import SettingsDef

product_root = Path(__file__).parent.resolve()


class AppSettings(SettingsDef):
    """Defines the default settings for flash cards app."""

    QUESTION_STORE_PATH: Path = Path.home() / "flash_cards" / "data" / "question_sets.json"
    GAME_STORE_PATH: Path = Path.home() / "flash_cards" / "data" / "games.json"
    SAMPLE_QUESTION_SETS: Path = product_root / "resources" / "sample_question_sets.json"
