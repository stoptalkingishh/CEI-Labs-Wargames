#!/usr/bin/env python3
"""Authorized local HTTP audit for the clean-room Natas 20-24 scenarios."""
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
    for level in range(20, 26):
        require(isinstance(values.get("natas%d" % level), str) and values["natas%d" % level], "missing adjacent test secret")
    return values


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


class Audit:
    def __init__(self, base, secrets):
        self.base, self.secrets = local_url(base), secrets

    def request(self, level, path="/", fields=None, headers=None, password=None, follow=True):
        secret = self.secrets["natas%d" % level] if password is None else password
        auth = base64.b64encode(("natas%d:" % level + secret).encode()).decode()
        data = urllib.parse.urlencode(fields, doseq=True).encode() if fields is not None else None
        request = urllib.request.Request(
            self.base.rsplit(":", 1)[0] + ":%d%s" % (urllib.parse.urlparse(self.base).port + level, path),
            data=data, headers={"Authorization": "Basic " + auth, **({"Content-Type": "application/x-www-form-urlencoded"} if data else {}), **(headers or {})},
        )
        opener = urllib.request.build_opener(NoRedirect) if not follow else urllib.request.build_opener()
        try:
            with opener.open(request, timeout=5) as response:
                return response.status, response.read(), response.headers
        except urllib.error.HTTPError as error:
            return error.code, error.read(), error.headers


def require_adjacent_only(body, level, secrets):
    for other in range(20, 26):
        if other != level + 1:
            require(secrets["natas%d" % other].encode() not in body, "nonadjacent secret exposed at %d" % level)


def main(base, secrets):
    audit = Audit(base, secrets)
    for level in range(20, 25):
        status, _, _ = audit.request(level, password="wrong")
        require(status == 401, "wrong authentication accepted at %d" % level)
        status, body, _ = audit.request(level, follow=False)
        require(status in (200, 302), "valid authentication rejected at %d" % level)
        require_adjacent_only(body, level, secrets)

    _, body, _ = audit.request(20, fields={"note": "hello"})
    require(secrets["natas21"].encode() not in body, "ordinary note elevated level 20")
    _, body, _ = audit.request(20, fields={"note": "hello|role=operator"})
    require(secrets["natas21"].encode() in body, "two-request record scenario failed")

    _, body, _ = audit.request(21, "/reports")
    require(secrets["natas22"].encode() not in body, "reports accepted no badge")
    _, _, headers = audit.request(21, "/desk?badge=operator")
    cookie = headers.get("Set-Cookie", "").split(";", 1)[0]
    _, body, _ = audit.request(21, "/reports", headers={"Cookie": cookie})
    require(secrets["natas22"].encode() in body, "cross-route intended path failed")
    _, body, _ = audit.request(21, "/other", headers={"Cookie": cookie})
    require(secrets["natas22"].encode() not in body, "unapproved route exposed a secret")

    status, body, headers = audit.request(22, "/?next=/receipt&run=review", follow=False)
    require(status == 302 and headers.get("Cache-Control") == "no-store", "redirect/no-store contract failed")
    require(secrets["natas23"].encode() in body, "redirect execution scenario failed")
    _, body, safe_headers = audit.request(22, "/?next=http://example.test&run=review", follow=False)
    require(safe_headers.get("Location") == "/receipt", "external redirect was accepted")

    _, body, _ = audit.request(23, fields={"token": "7x"})
    require(secrets["natas24"].encode() in body and b"Strict control: denied." in body, "numeric-prefix intended path failed")
    for token, description in (("7", "canonical"), ("x7", "alphabetic"), ("", "empty")):
        _, body, _ = audit.request(23, fields={"token": token})
        require(secrets["natas24"].encode() not in body, "%s numeric token released level 24" % description)

    _, body, _ = audit.request(24, fields=[("access[role]", "operator"), ("access[region]", "local")])
    require(secrets["natas25"].encode() in body, "structured request intended path failed")
    _, body, _ = audit.request(24, fields={"access": "operator"})
    require(secrets["natas25"].encode() not in body, "scalar shape elevated level 24")
    _, body, _ = audit.request(24, fields=[("access[role]", "operator"), ("access[region]", "remote")])
    require(secrets["natas25"].encode() not in body, "wrong structured model elevated level 24")
    print("NATAS_LEVELS_20_THROUGH_24_OK")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--secrets", required=True)
    args = parser.parse_args()
    try:
        main(args.base_url, parse_secrets(args.secrets))
    except (AssertionError, ValueError, urllib.error.URLError) as error:
        raise SystemExit("NATAS_20_24_AUDIT_FAILED: %s" % error)
