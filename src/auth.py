import os
import hmac
import hashlib

import flask

ALLOWED_USERS = os.getenv("ALLOWED_USERS", "*").split(",")
SECRET = os.getenv("SECRET")

assert not (SECRET is None or SECRET == "REPLACE_WITH_YOUR_SECRET_KEY")


def is_authorized_user(user: str) -> bool:
    return user in ALLOWED_USERS or "*" in ALLOWED_USERS


def verify_signature(request: flask.Request) -> bool:
    # As described here:
    # https://docs.github.com/en/webhooks-and-events/webhooks/securing-your-webhooks#python-example

    if signature_header := request.headers.get("X-Hub-Signature-256") is None:
        return False

    hash_object = hmac.new(SECRET.encode('utf-8'), msg=request.data, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)
