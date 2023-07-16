from helpers import *

from flask import Flask

clone_repos()
app = Flask(__name__)


@app.route("/webhook/<webhook_name>")
def trigger_build(webhook_name: str):
    if webhook_name not in CONFIG.keys():
        return "No such repository configured.", 404

    repo_path = REPO_DIR / webhook_name
    if not repo_has_changes(repo_path):
        return "No changes detected. Go for a walk, come back, make some changes, push :)", 420
    pull(repo_path)

    return "Done"


if __name__ == "__main__":
    app.run("0.0.0.0", 54321)
    delete_repos()
