from helpers import *

from flask import Flask

clone_repos()
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, world!"
