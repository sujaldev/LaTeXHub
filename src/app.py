from helpers import *

from flask import Flask

clone_repos()
app = Flask(__name__)


@app.route("/webhook/<webhook_name>")
def trigger_build(webhook_name: str):
    if webhook_name not in CONFIG.keys():
        return "No such repository configured.", 404

    return "Done"


if __name__ == "__main__":
    app.run("0.0.0.0", 54321)
    delete_repos()
