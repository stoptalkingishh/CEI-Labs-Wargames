#!/usr/bin/env python3
"""Render deterministic, per-team Sentinel evidence before sshd starts."""

import hashlib
import json
import os
import subprocess

KEYS = ("sentinel-start-here", "sentinel-01", "sentinel-02", "sentinel-03", "sentinel-04", "sentinel-05")


def derived(secret, label, length=16):
    return hashlib.sha256(f"sentinel:{label}:{secret}".encode()).hexdigest()[:length]


def load_secrets():
    try:
        secrets = json.loads(os.environ["LEVEL_SECRETS"])
    except (KeyError, json.JSONDecodeError) as error:
        raise SystemExit("LEVEL_SECRETS is required and must be valid JSON") from error
    missing = [key for key in KEYS if not isinstance(secrets.get(key), str) or not secrets[key]]
    if missing:
        raise SystemExit("LEVEL_SECRETS is missing required Sentinel keys")
    return secrets


def write(owner, name, text):
    path = f"/home/{owner}/{name}"
    with open(path, "w", encoding="utf-8", newline="\n") as output:
        output.write(text)
    subprocess.run(["chown", f"{owner}:{owner}", path], check=True)
    os.chmod(path, 0o400)


def main():
    secrets = load_secrets()
    for number, key in enumerate(KEYS[:-1], 1):
        subprocess.run(["chpasswd"], input=f"sentinel{number}:{secrets[key]}\n", text=True, check=True)

    write("sentinel0", "ENGAGEMENT-RULES.txt", "Northstar training host: inspect only local evidence. Do not alter services or access other systems.\nonboarding-token=" + secrets["sentinel-start-here"] + "\ncase-id=" + derived(secrets["sentinel-start-here"], "onboarding") + "\n")
    write("sentinel1", "asset-census.txt", "Asset inventory: northstar-jump-01\nInstalled package review: openssh-server approved\nActive service review: ssh.service approved\nOwnership review: /etc/ssh/sshd_config root:root\ncensus-result=" + secrets["sentinel-01"] + "\nrecord-id=" + derived(secrets["sentinel-01"], "asset") + "\n")
    write("sentinel2", "controls.md", "MFA: technical preventive\nBadge review: physical preventive\nLog review: technical detective\n")
    write("sentinel2", "control-evidence.md", "Evidence confirms the listed safeguards are implemented.\napproved-review-result=" + secrets["sentinel-02"] + "\nreview-id=" + derived(secrets["sentinel-02"], "control") + "\n")
    write("sentinel3", "change-window.txt", "Change: rotate jump-host certificate\nApproval: missing change-owner signature\nTesting: attached\nRollback: attached\nBoard disposition: DEFER\nrecorded-disposition=" + secrets["sentinel-03"] + "\nchange-id=" + derived(secrets["sentinel-03"], "change") + "\n")
    write("sentinel4", "certificate-ledger.txt", "Service: ops.northstar.training\nIssuer: Northstar Training CA\nRevocation: clear\nKey permissions: owner-read-only\nverified-service-record=" + secrets["sentinel-04"] + "\nserial=" + derived(secrets["sentinel-04"], "certificate") + "\n")
    write("sentinel5", "exposure-review.conf", "Observed listener: ssh tcp/22\nConfigured default service: legacy-metrics disabled\nNo web, database, or remote-management service is exposed.\nsigned-finding=" + secrets["sentinel-05"] + "\nreview-id=" + derived(secrets["sentinel-05"], "surface") + "\n")


if __name__ == "__main__":
    main()
