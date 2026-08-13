#!/usr/bin/env python3
"""Authorized local HTTP audit for the clean-room Natas 15-19 scenarios."""
import argparse
import base64
import json
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request


def require(value, message):
    if not value:
        raise AssertionError(message)


def local_url(value):
    parsed = urllib.parse.urlparse(value)
    require(parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}, "base URL must be loopback HTTP")
    require(parsed.port and not parsed.path.rstrip("/"), "base URL must contain only host and port")
    return value.rstrip("/")


def parse_secrets(raw):
    values = json.loads(raw)
    require(isinstance(values, dict), "secrets must be an object")
    for level in range(15, 21):
        require(isinstance(values.get("natas%d" % level), str) and values["natas%d" % level], "missing adjacent test secret")
    return values


class Audit:
    def __init__(self, base, secrets): self.base, self.secrets = local_url(base), secrets
    def request(self, level, path="/", data=None, headers=None, password=None):
        secret = self.secrets["natas%d" % level] if password is None else password
        auth = base64.b64encode(("natas%d:" % level + secret).encode()).decode()
        request = urllib.request.Request(self.base.rsplit(":", 1)[0] + ":%d%s" % (urllib.parse.urlparse(self.base).port + level, path), data=data, headers={"Authorization": "Basic " + auth, **(headers or {})})
        try:
            with urllib.request.urlopen(request, timeout=5) as response: return response.status, response.read(), response.headers
        except urllib.error.HTTPError as error: return error.code, error.read(), error.headers
    def form(self, level, fields):
        return self.request(level, "/", urllib.parse.urlencode(fields).encode(), {"Content-Type": "application/x-www-form-urlencoded"})


def main(base, secrets):
    audit = Audit(base, secrets)
    for level in range(15, 20):
        status, _, _ = audit.request(level, password="wrong")
        require(status == 401, "wrong authentication accepted at %d" % level)
    for level in range(15, 20):
        status, body, _ = audit.request(level)
        require(status == 200, "valid authentication rejected at %d" % level)
        for other in range(15, 21):
            if other != level + 1: require(secrets["natas%d" % other].encode() not in body, "nonadjacent secret exposed at %d" % level)

    prefix = secrets["natas16"][:1]
    _, body, _ = audit.form(15, {"probe": "account=operator; prefix=" + prefix})
    require(b"Record exists." in body, "boolean oracle intended path failed")
    _, body, _ = audit.request(16, "/?needle=catalog%20credential")
    require(secrets["natas17"].encode() in body, "emulator intended path failed")
    measurements = []
    for candidate in ("wrong", secrets["natas18"][:1]):
        samples = []
        for _ in range(2):
            started = time.monotonic(); audit.form(17, {"prefix": candidate}); samples.append(time.monotonic() - started)
        measurements.append(statistics.mean(samples))
    require(measurements[1] > measurements[0] + .07, "timing oracle intended path failed")
    _, body, _ = audit.request(18, headers={"Cookie": "CEI18=42"})
    require(secrets["natas19"].encode() in body, "numeric session intended path failed")
    token = base64.urlsafe_b64encode(b"id=1;role=operator").decode().rstrip("=")
    _, body, _ = audit.request(19, headers={"Cookie": "CEI19=" + token})
    require(secrets["natas20"].encode() in body, "token codec intended path failed")
    print("NATAS_LEVELS_15_THROUGH_19_OK")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--secrets", required=True)
    args = parser.parse_args()
    try: main(args.base_url, parse_secrets(args.secrets))
    except (AssertionError, ValueError, urllib.error.URLError) as error: raise SystemExit("NATAS_15_19_AUDIT_FAILED: %s" % error)
