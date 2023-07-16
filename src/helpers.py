import tomllib
from pathlib import Path
from subprocess import run

APP_DIR = Path(__file__).parent.parent
CONFIG_DIR = APP_DIR / "config/"
REPO_DIR = APP_DIR / "repos/"

with open(CONFIG_DIR / "config.toml", "rb") as file:
    CONFIG = tomllib.load(file)
