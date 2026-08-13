#!/usr/bin/env python3
"""Authorized local HTTP audit for clean-room Natas 25-29 scenarios."""
import argparse
import base64
import json
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
    for level in range(25, 31):
        require(isinstance(values.get("natas%d" % level), str) and values["natas%d" % level], "missing adjacent test secret")
    return values


class Audit:
    def __init__(self, base, secrets): self.base, self.secrets = local_url(base), secrets
    def request(self, level, fields=None, password=None):
        secret = self.secrets["natas%d" % level] if password is None else password
        auth = base64.b64encode(("natas%d:" % level + secret).encode()).decode()
        data = urllib.parse.urlencode(fields or {}).encode()
        request = urllib.request.Request(self.base.rsplit(":", 1)[0] + ":%d/" % (urllib.parse.urlparse(self.base).port + level), data=data, headers={"Authorization": "Basic " + auth, "Content-Type": "application/x-www-form-urlencoded"})
        try:
            with urllib.request.urlopen(request, timeout=5) as response: return response.status, response.read()
        except urllib.error.HTTPError as error: return error.code, error.read()


def require_adjacent_only(body, level, secrets):
    for other in range(25, 31):
        if other != level + 1: require(secrets["natas%d" % other].encode() not in body, "nonadjacent secret exposed at %d" % level)


def main(base, secrets):
    audit = Audit(base, secrets)
    for level in range(25, 30):
        status, _ = audit.request(level, password="wrong")
        require(status == 401, "wrong authentication accepted at %d" % level)
        status, body = audit.request(level)
        require(status == 200, "valid authentication rejected at %d" % level)
        require_adjacent_only(body, level, secrets)
    cases = {25: ({"marker": "audit:handoff"}, {"marker": "../../etc/passwd"}), 26: ({"project": '{"project":{"export":"handoff"}}'}, {"project": '{"project":{"export":"handoff","extra":true}}'}), 27: ({"identity": "ops.lead"}, {"identity": "operator"}), 28: ({"token": "VISITOR-ATOROPER"}, {"token": "VISITOR-OPERATORS"}), 29: ({"filename": "handoff.log|catalog:handoff"}, {"filename": "handoff.log|catalog:other"})}
    for level, (positive, negative) in cases.items():
        _, body = audit.request(level, positive)
        require(secrets["natas%d" % (level + 1)].encode() in body, "intended path failed at %d" % level)
        _, body = audit.request(level, negative)
        require(secrets["natas%d" % (level + 1)].encode() not in body, "negative path released secret at %d" % level)
    print("NATAS_LEVELS_25_THROUGH_29_OK")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--secrets", required=True)
    args = parser.parse_args()
    try: main(args.base_url, parse_secrets(args.secrets))
    except (AssertionError, ValueError, urllib.error.URLError) as error: raise SystemExit("NATAS_25_29_AUDIT_FAILED: %s" % error)
