#!/usr/bin/env python3
"""One-time bootstrap for the local CTFd instance started by
docker-compose.yml in this directory: runs the /setup wizard in teams mode,
logs in as the resulting admin, and mints an API token.

Prints `CTFD_URL=...` and `CTFD_TOKEN=...` lines to stdout so callers can
eval them into the environment.
"""
import re
import sys

import requests

BASE_URL = "http://localhost:8000"
CTF_NAME = "CEI Labs Local Test"
ADMIN_NAME = "admin"
ADMIN_EMAIL = "admin@ctf.local"
ADMIN_PASSWORD = "LocalTest-Passw0rd!"


def _nonce(html: str) -> str:
    match = re.search(r'name="nonce"[^>]*value="([a-f0-9]+)"', html)
    if not match:
        match = re.search(r'value="([a-f0-9]+)"[^>]*name="nonce"', html)
    if not match:
        # Authenticated pages (e.g. /settings) embed it as a JS var instead
        # of a form field: 'csrfNonce': "<hex>".
        match = re.search(r"csrfNonce['\"]?\s*:\s*[\"']([a-f0-9]+)[\"']", html)
    if not match:
        raise RuntimeError("could not find CSRF nonce in response")
    return match.group(1)


def main() -> int:
    session = requests.Session()

    setup_page = session.get(f"{BASE_URL}/setup")
    if setup_page.status_code != 200:
        print(f"already set up or unreachable (HTTP {setup_page.status_code}); trying login instead", file=sys.stderr)
    else:
        nonce = _nonce(setup_page.text)
        resp = session.post(
            f"{BASE_URL}/setup",
            data={
                "nonce": nonce,
                "ctf_name": CTF_NAME,
                "ctf_description": "Local black-box test instance",
                "name": ADMIN_NAME,
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD,
                "user_mode": "teams",
                "setup": "true",
            },
            allow_redirects=True,
        )
        if resp.status_code != 200:
            print(f"setup POST failed: HTTP {resp.status_code}", file=sys.stderr)
            return 1

    login_page = session.get(f"{BASE_URL}/login")
    nonce = _nonce(login_page.text)
    login_resp = session.post(
        f"{BASE_URL}/login",
        data={"name": ADMIN_NAME, "password": ADMIN_PASSWORD, "nonce": nonce},
        allow_redirects=True,
    )
    if "incorrect" in login_resp.text.lower() and login_resp.url.endswith("/login"):
        print("login failed", file=sys.stderr)
        return 1

    settings_page = session.get(f"{BASE_URL}/settings")
    nonce = _nonce(settings_page.text)
    token_resp = session.post(
        f"{BASE_URL}/api/v1/tokens",
        json={"expiration": "2030-01-01", "description": "local smoke-test automation"},
        headers={"CSRF-Token": nonce},
    )
    token_resp.raise_for_status()
    token = token_resp.json()["data"]["value"]

    print(f"CTFD_URL={BASE_URL}")
    print(f"CTFD_TOKEN={token}")
    print(f"CTFD_ADMIN_NAME={ADMIN_NAME}", file=sys.stderr)
    print(f"CTFD_ADMIN_PASSWORD={ADMIN_PASSWORD}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
