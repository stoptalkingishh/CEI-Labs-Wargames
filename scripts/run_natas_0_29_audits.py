#!/usr/bin/env python3
"""Run every authorized local Natas audit through one isolated target.

The auditors address level N as base-port + N, so this runner reserves and
publishes one contiguous loopback range for ports 8000 through 8034.
"""
import base64
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid


IMAGE = "cei-labs-natas-0-29-audit"
CONTAINER = "cei-labs-natas-0-29-audit"
FIRST_PORT = 20000
LAST_PORT = 60000
LEVEL_COUNT = 35


def run(*args, check=True, **kwargs):
    return subprocess.run(args, check=check, text=True, **kwargs)


def free_port_base():
    for base in range(FIRST_PORT, LAST_PORT - LEVEL_COUNT, LEVEL_COUNT):
        sockets = []
        try:
            for port in range(base, base + LEVEL_COUNT):
                listener = socket.socket()
                listener.bind(("127.0.0.1", port))
                sockets.append(listener)
            return base
        except OSError:
            pass
        finally:
            for listener in sockets:
                listener.close()
    raise RuntimeError("no contiguous loopback port range is available")


def request(base, secrets):
    auth = base64.b64encode(b"natas0:natas0").decode()
    request = urllib.request.Request("http://127.0.0.1:%d/" % base, headers={"Authorization": "Basic " + auth})
    with urllib.request.urlopen(request, timeout=2) as response:
        if response.status != 200:
            raise RuntimeError("level 0 returned unexpected status")


def wait_for_apache(base, secrets):
    for _ in range(60):
        try:
            request(base, secrets)
            return
        except (OSError, urllib.error.URLError, RuntimeError):
            time.sleep(1)
    raise RuntimeError("Apache did not become reachable on the published level-0 port")


def audit_command(script, base, secrets):
    return (sys.executable, os.path.join(os.path.dirname(__file__), script), "--base-url", "http://127.0.0.1:%d" % base, "--secrets", json.dumps(secrets))


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    secrets = {"natas%d" % level: "SWEEP_%d_%s" % (level, uuid.uuid4().hex) for level in range(1, 35)}
    secrets["natas14final"] = "SWEEP_FINAL_%s" % uuid.uuid4().hex
    base = free_port_base()
    publishes = [item for level in range(LEVEL_COUNT) for item in ("--publish", "127.0.0.1:%d:%d" % (base + level, 8000 + level))]
    run("docker", "build", "--tag", IMAGE, "targets/natas", cwd=root)
    run("docker", "rm", "--force", CONTAINER, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        run("docker", "run", "--detach", "--name", CONTAINER, "--env", "NATAS_TARGET_TEAM=full-audit", "--env", "LEVEL_SECRETS=" + json.dumps(secrets), *publishes, IMAGE, stdout=subprocess.DEVNULL)
        wait_for_apache(base, secrets)
        run(*audit_command("runtime_audit_natas.py", base, secrets), cwd=root)
        run(*audit_command("runtime_audit_natas_15_19.py", base, {key: secrets[key] for key in ("natas15", "natas16", "natas17", "natas18", "natas19", "natas20")}), cwd=root)
        run(*audit_command("runtime_audit_natas_20_24.py", base, {key: secrets[key] for key in ("natas20", "natas21", "natas22", "natas23", "natas24", "natas25")}), cwd=root)
        run(*audit_command("runtime_audit_natas_25_29.py", base, {key: secrets[key] for key in ("natas25", "natas26", "natas27", "natas28", "natas29", "natas30")}), cwd=root)
        print("NATAS_LEVELS_0_THROUGH_29_SWEEP_OK")
    finally:
        run("docker", "rm", "--force", CONTAINER, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, subprocess.CalledProcessError, urllib.error.URLError) as error:
        print("NATAS_0_29_SWEEP_FAILED: %s" % error, file=sys.stderr)
        raise SystemExit(1)
