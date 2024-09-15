"""Pytest Configuration File."""

import sys
from pathlib import Path

import pyapp.conf

HERE = Path(__file__).absolute()
SRC_PATH = HERE.parent.parent / "src"
sys.path.insert(0, SRC_PATH.as_posix())

pyapp.conf.settings.configure("flash_cards.default_settings")
