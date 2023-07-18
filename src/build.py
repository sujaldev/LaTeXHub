import os
import shutil
import tomllib
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from git import Repo

APP_DIR = Path(__file__).parent.parent.parent.resolve()
REPO_DIR = APP_DIR / "repos/"
BUILD_DIR = APP_DIR / "build/"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
assert not (GITHUB_TOKEN is None or GITHUB_TOKEN == "REPLACE_WITH_YOUR_GITHUB_TOKEN")


class Builder:
    DEFAULT_CONFIG_FILE = "latexhub.toml"
    DEFAULT_BUILD_FILE = "build.sh"
    DEFAULT_ARTIFACT_DIR = "build/"

    def __init__(self, user: str, repo: str):
        self.user = user
        self.repo = repo

        self.repo_path = REPO_DIR / f"{user}/{repo}"

        self.branch = Repo(self.repo_path).active_branch.tracking_branch().remote_head

        self.config = {
            "build": {
                "script": self.DEFAULT_BUILD_FILE,
                "artifact_dir": self.DEFAULT_ARTIFACT_DIR,
            }
        }

    @property
    def build_script(self):
        return self.config.get("build", {}).get("script", self.DEFAULT_BUILD_FILE)

    @property
    def artifact_dir(self):
        return self.config.get("build", {}).get("artifact_dir", self.DEFAULT_ARTIFACT_DIR)

    def load_config(self, tmp_path: Path):
        conf_path = tmp_path / self.DEFAULT_CONFIG_FILE

        if conf_path.exists():
            with open(conf_path, "rb") as config_file:
                self.config = tomllib.load(config_file)

    def parse_include_script(self, script: str) -> str:
        replace_map = {
            "USER": self.user,
            "REPO": self.repo,
            "BRANCH": self.branch,
            "GITHUB_TOKEN": GITHUB_TOKEN,
        }

        for old, new in replace_map.items():
            script = script.replace(f"%%{old}%%", new)

        return script

    def run_build_script(self, tmp_path: Path):
        # Imports include.sh and runs the build script.

        script_path = tmp_path / self.build_script
        include_script_path = Path(__file__).parent / "include.sh"

        with open(include_script_path) as include_script_file:
            include_script = include_script_file.read() + "\n\n"

        with open(script_path, "r+") as script_file:
            build_script = include_script + script_file.read()
            script_file.seek(0)
            script_file.write(build_script)

        # Ensure artifact directory exists (just in case the build script does not create it)
        (tmp_path / self.artifact_dir).mkdir(exist_ok=True)
        subprocess.run(["/bin/bash", script_path], cwd=tmp_path)

    def build(self):
        with TemporaryDirectory() as tmpdir:
            shutil.copytree(self.repo_path, tmpdir, dirs_exist_ok=True)

            tmp_path = Path(tmpdir)
            self.load_config(tmp_path)
            self.run_build_script(tmp_path)

            # Copy Generated Artifacts
            shutil.copytree(tmp_path / self.artifact_dir, BUILD_DIR, dirs_exist_ok=True)
