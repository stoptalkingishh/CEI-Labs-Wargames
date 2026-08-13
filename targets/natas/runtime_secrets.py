"""Validate and safely materialize Natas's per-team startup secrets."""

import base64
import json
import os
import sys

# Unit tests load this module from the target source directory, while the
# image installs natas_levels.py alongside it in /usr/local/lib.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "build"))
from natas_levels import REQUIRED_SECRET_KEYS


REQUIRED_KEYS = REQUIRED_SECRET_KEYS


def load_required_secrets(raw_secrets):
    """Return valid secrets or fail without exposing their values."""
    try:
        secrets = json.loads(raw_secrets)
    except (TypeError, ValueError) as error:
        raise ValueError("LEVEL_SECRETS must be valid JSON") from error

    if not isinstance(secrets, dict) or set(secrets) != REQUIRED_KEYS:
        raise ValueError("LEVEL_SECRETS must be an object with exactly the required Natas keys")

    for key, value in secrets.items():
        if not isinstance(value, str) or not value or any(ord(char) < 32 or ord(char) == 127 for char in value):
            raise ValueError(f"LEVEL_SECRETS entry {key} must be a nonempty safe string")
    return secrets


def write_php_secret(path, variable_name, value):
    """Write a PHP value without treating a secret as PHP source text."""
    encoded = base64.b64encode(value.encode("utf-8")).decode("ascii")
    with open(path, "w") as secret_file:
        secret_file.write(f"<?php\n${variable_name} = base64_decode('{encoded}');\n")


if __name__ == "__main__":
    try:
        load_required_secrets(os.environ.get("LEVEL_SECRETS"))
    except ValueError as error:
        print(f"Natas startup refused: {error}", file=sys.stderr)
        raise SystemExit(1)
