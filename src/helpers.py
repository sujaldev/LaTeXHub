import tomllib
from pathlib import Path
from subprocess import run

APP_DIR = Path(__file__).parent.parent
CONFIG_DIR = APP_DIR / "config/"
REPO_DIR = APP_DIR / "repos/"

with open(CONFIG_DIR / "config.toml", "rb") as file:
    CONFIG = tomllib.load(file)


def clone_repos():
    for repo, data in CONFIG.items():
        repo_url = data["repo"]
        run(["git", "clone", repo_url, REPO_DIR / repo])


def delete_repos():
    run(["rm", "-rf", REPO_DIR])
