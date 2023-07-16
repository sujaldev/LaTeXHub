import tomllib
from pathlib import Path
from subprocess import run, check_output

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


def repo_has_changes(repo_path: Path | str):
    run(["git", "remote", "update"], cwd=repo_path)
    branch = check_output(["git", "branch", "--show-current"]).decode().strip()
    remote = check_output(["git", "rev-parse", f"origin/{branch}"], cwd=repo_path).strip()
    local = check_output(["git", "rev-parse", branch], cwd=repo_path).strip()
    return remote != local


def pull(repo_path: Path | str):
    run(["git", "pull"], cwd=repo_path)
