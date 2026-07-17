"""Small black-box CTFd client shared by the staggered-scoring test scripts
in this directory's parent (test_staggered_smoke.py, test_staggered_concurrency.py,
test_export_reconciliation.py).

Talks to CTFd purely over HTTP the way a browser session or ctfcli would --
no direct DB access, no imports from cei-labs-engine's plugin code (except a
single read-only introspection helper below, see its docstring). Session
cookies + CTFd's own CSRF nonce, exactly like the admin panel and player UI.
"""
from __future__ import annotations

import re
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any

import requests

NONCE_INPUT_RE = re.compile(r'name="nonce"[^>]*value="([a-f0-9]+)"')
NONCE_INPUT_RE_ALT = re.compile(r'value="([a-f0-9]+)"[^>]*name="nonce"')
NONCE_JS_RE = re.compile(r"csrfNonce['\"]?\s*:\s*[\"']([a-f0-9]+)[\"']")


def extract_nonce(html: str) -> str:
    for pattern in (NONCE_INPUT_RE, NONCE_INPUT_RE_ALT, NONCE_JS_RE):
        match = pattern.search(html)
        if match:
            return match.group(1)
    raise RuntimeError("could not find a CSRF nonce in the response body")


@dataclass
class CTFdSession:
    """One authenticated CTFd session (cookie jar + CSRF nonce) -- used both
    for the admin session and for each simulated participant session."""

    base_url: str
    session: requests.Session = field(default_factory=requests.Session)
    nonce: str | None = None

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}{path}"

    def refresh_nonce(self, path: str = "/") -> str:
        resp = self.session.get(self._url(path))
        self.nonce = extract_nonce(resp.text)
        return self.nonce

    def login(self, name: str, password: str) -> None:
        resp = self.session.get(self._url("/login"))
        nonce = extract_nonce(resp.text)
        resp = self.session.post(
            self._url("/login"),
            data={"name": name, "password": password, "nonce": nonce},
            allow_redirects=True,
        )
        if resp.url.rstrip("/").endswith("/login"):
            raise RuntimeError(f"login failed for user {name!r}: {resp.status_code} {resp.url}")
        # The nonce stays constant for the life of the Flask session unless
        # regenerated (see CTFd's csrf() before_request hook), so one fetch
        # right after login is enough for every subsequent state change.
        self.refresh_nonce("/")

    # -- generic form-encoded admin/plugin POST (nonce injected automatically) --
    def admin_post(self, path: str, data: dict[str, Any] | None = None) -> requests.Response:
        payload = dict(data or {})
        payload["nonce"] = self.nonce
        return self.session.post(self._url(path), data=payload, allow_redirects=True)

    # -- JSON CTFd core API (CSRF-Token header, matching content_type == application/json) --
    def api(self, method: str, path: str, json: Any = None) -> requests.Response:
        headers = {"CSRF-Token": self.nonce} if self.nonce else {}
        return self.session.request(method, self._url(path), json=json, headers=headers)

    def get(self, path: str, **kw) -> requests.Response:
        return self.session.get(self._url(path), **kw)


def bootstrap_admin(base_url: str, name: str, password: str) -> CTFdSession:
    admin = CTFdSession(base_url=base_url)
    admin.login(name, password)
    return admin


# -- CTFd core admin API helpers -------------------------------------------------

def create_user(admin: CTFdSession, name: str, email: str, password: str) -> int:
    resp = admin.api("POST", "/api/v1/users", json={
        "name": name, "email": email, "password": password,
        "type": "user", "verified": True, "banned": False, "hidden": False,
    })
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"create_user({name!r}) failed: {body}")
    return body["data"]["id"]


def create_team(admin: CTFdSession, name: str, password: str) -> int:
    resp = admin.api("POST", "/api/v1/teams", json={"name": name, "password": password})
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"create_team({name!r}) failed: {body}")
    return body["data"]["id"]


def add_team_member(admin: CTFdSession, team_id: int, user_id: int) -> None:
    resp = admin.api("POST", f"/api/v1/teams/{team_id}/members", json={"user_id": user_id})
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"add_team_member(team={team_id}, user={user_id}) failed: {body}")


def get_challenge_id(admin: CTFdSession, name: str) -> int:
    resp = admin.api("GET", "/api/v1/challenges?view=admin&per_page=100")
    resp.raise_for_status()
    body = resp.json()
    for row in body["data"]:
        if row["name"] == name:
            return row["id"]
    raise RuntimeError(f"no challenge named {name!r} found")


def add_static_flag(admin: CTFdSession, challenge_id: int, content: str) -> None:
    """Adds an extra `static` flag to a challenge alongside whatever
    per_team_dynamic* flag deploy.sh installed. CTFd accepts a submission if
    ANY of a challenge's flags match, so this lets black-box tests exercise
    real solve/scoreboard behavior without needing a live orchestrator to
    mint per-team secrets (out of scope here -- see docs/staggered-wargame-
    stage-verification.md, which assumes a full Engine deployment)."""
    resp = admin.api("POST", "/api/v1/flags", json={
        "challenge_id": challenge_id, "content": content, "type": "static", "data": "",
    })
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success"):
        raise RuntimeError(f"add_static_flag(challenge={challenge_id}) failed: {body}")


def submit_flag(participant: CTFdSession, challenge_id: int, flag: str) -> dict:
    resp = participant.api("POST", "/api/v1/challenges/attempt", json={
        "challenge_id": challenge_id, "submission": flag,
    })
    resp.raise_for_status()
    return resp.json()


# -- wargame-stages plugin -------------------------------------------------------

def stage_sync(admin: CTFdSession, slug: str) -> requests.Response:
    return admin.admin_post(f"/plugins/wargame-stages/admin/{slug}/sync")


def stage_start(admin: CTFdSession, slug: str) -> requests.Response:
    return admin.admin_post(f"/plugins/wargame-stages/admin/{slug}/start")


def stage_lock(admin: CTFdSession, slug: str) -> requests.Response:
    return admin.admin_post(f"/plugins/wargame-stages/admin/{slug}/lock")


def stage_close(admin: CTFdSession, slug: str) -> requests.Response:
    return admin.admin_post(f"/plugins/wargame-stages/admin/{slug}/close")


def stage_visibility(admin: CTFdSession, slug: str, visible: bool) -> requests.Response:
    return admin.admin_post(f"/plugins/wargame-stages/admin/{slug}/visibility", data={"visible": "true" if visible else "false"})


def stage_export(admin: CTFdSession, slug: str, fmt: str = "json") -> requests.Response:
    return admin.get(f"/plugins/wargame-stages/admin/{slug}/export.{fmt}")


def scoreboard_page(session: CTFdSession, slug: str) -> requests.Response:
    return session.get(f"/plugins/wargame-stages/{slug}/scoreboard")


# -- direct DB read-only introspection -------------------------------------------
# The wargame-stages plugin exposes no HTTP endpoint for the audit trail (only
# rendered into the admin HTML template), so "confirm the audit table has only
# one start mutation" (docs/staggered-wargame-stage-verification.md item 4) has
# no other black-box-observable surface. This shells out to the DB container
# read-only via `docker exec ... mysql -e SELECT ...` -- never INSERT/UPDATE/DELETE.

def audit_count(db_container: str, db_user: str, db_password: str, db_name: str, slug: str, action: str) -> int:
    query = (
        "SELECT COUNT(*) FROM wargame_stage_audit a "
        "JOIN wargame_stages s ON a.stage_id = s.id "
        f"WHERE s.slug = '{slug}' AND a.action = '{action}';"
    )
    result = subprocess.run(
        ["docker", "exec", db_container, "mysql", f"-u{db_user}", f"-p{db_password}", db_name, "-N", "-e", query],
        capture_output=True, text=True, check=True,
    )
    return int(result.stdout.strip())


def wait_until(predicate, timeout=15, interval=0.5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()
