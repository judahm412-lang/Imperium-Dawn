"""Writable user storage, independent of installation location."""
import os
from pathlib import Path


def save_path():
    root = Path(os.environ.get('XDG_DATA_HOME') or Path.home() / '.local' / 'share')
    directory = root / 'imperium-dawn'
    directory.mkdir(parents=True, exist_ok=True)
    return directory / 'savegame.json'
