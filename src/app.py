from build import Builder
from git_helpers import rebuild_is_required
from env import is_authorized_user, verify_signature

from flask import Flask, request

app = Flask(__name__)


@app.route("/webhook/<user>/<repo>")
def trigger_build(user: str, repo: str):
    if not verify_signature(request):
        return "Incorrect signature.", 403

    if not is_authorized_user(user):
        return "This user/organization is not permitted to trigger a build.", 403

    if not rebuild_is_required(user, repo):
        return "No changes detected, rebuild not required."

    Builder(user, repo).build()
    return "Done!"


if __name__ == "__main__":
    app.run("0.0.0.0", 54321)
