from pathlib import Path
from typing import NamedTuple, Dict

app_path_abs = Path(__file__).resolve().parent.parent

class PomodoroPaths(NamedTuple):
    icon: Path
    stats_dir: Path
    sounds: Dict

paths = PomodoroPaths(
    icon=app_path_abs.joinpath("icons/tomato.png"),
    stats_dir=app_path_abs.joinpath("stats"),
    sounds={ "ringbell" : str(app_path_abs.joinpath("sounds/bell_sound.mp3")) }
)
