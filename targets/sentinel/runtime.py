#!/usr/bin/env python3
"""Render deterministic, per-team Sentinel evidence before sshd starts."""

import hashlib
import json
import os
import subprocess

KEYS = ("sentinel-start-here", "sentinel-01", "sentinel-02", "sentinel-03", "sentinel-04", "sentinel-05")

ANSWERS = {
    "sentinel-start-here": {"engagement_scope": "local-evidence-only"},
    "sentinel-01": {"asset": "northstar-jump-01", "package": "openssh-server", "service": "sshd", "owner": "root:root"},
    "sentinel-02": {"mfa": "technical-preventive", "badge_review": "physical-preventive", "log_review": "technical-detective"},
    "sentinel-03": {"disposition": "DEFER", "missing_evidence": "change-owner-signature"},
    "sentinel-04": {"service": "ops.northstar.training", "issuer": "Northstar Training Test CA", "revocation_status": "clear", "key_mode": "0400"},
    "sentinel-05": {"listener": "ssh", "port": 22, "legacy_metrics": "disabled"},
}


def derived(secret, label, length=16):
    return hashlib.sha256(f"sentinel:{label}:{secret}".encode()).hexdigest()[:length]


def load_secrets():
    try:
        secrets = json.loads(os.environ["LEVEL_SECRETS"])
    except (KeyError, json.JSONDecodeError) as error:
        raise SystemExit("LEVEL_SECRETS is required and must be valid JSON") from error
    if not isinstance(secrets, dict):
        raise SystemExit("LEVEL_SECRETS must be a JSON object with required Sentinel keys")
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


def write_root(name, text):
    path = f"/var/lib/sentinel/{name}"
    with open(path, "w", encoding="utf-8", newline="\n") as output:
        output.write(text)
    os.chown(path, 0, 0)
    os.chmod(path, 0o600)


def main():
    secrets = load_secrets()
    for number, key in enumerate(KEYS[:-1], 1):
        subprocess.run(["chpasswd"], input=f"sentinel{number}:{secrets[key]}\n", text=True, check=True)

    write_root("credentials.json", json.dumps(secrets))
    write_root("answers.json", json.dumps(ANSWERS))

    write("sentinel0", "ENGAGEMENT-RULES.txt", "Northstar training host: inspect only local evidence. Do not alter services or access other systems.\nSubmit this structured answer with `sentinel-submit`: {\"lab\": \"sentinel-start-here\", \"answer\": {\"engagement_scope\": \"local-evidence-only\"}}\n")
    write("sentinel0", "asset-census.txt", "Asset inventory: northstar-jump-01\nInstalled package review: openssh-server approved\nActive service review: sshd approved\nOwnership review: /etc/ssh/sshd_config root:root\nSubmit the asset, package, service, and owner fields through `sentinel-submit`.\n")
    write("sentinel1", "controls.md", "MFA: technical preventive\nBadge review: physical preventive\nLog review: technical detective\n")
    write("sentinel1", "control-evidence.md", "Evidence confirms the listed safeguards are implemented.\nSubmit the MFA, badge-review, and log-review classifications through `sentinel-submit`.\n")
    write("sentinel2", "change-window.txt", "Change: rotate jump-host certificate\nApproval: missing change-owner signature\nTesting: attached\nRollback: attached\nBoard disposition: DEFER\nSubmit the disposition and missing-evidence fields through `sentinel-submit`.\n")
    for name in ("training-ca.pem", "service.pem", "training-ca.crl"):
        with open(f"/opt/sentinel/certs/{name}", encoding="utf-8") as source:
            write("sentinel3", name, source.read())
    subprocess.run(["cp", "/opt/sentinel/certs/service.key", "/home/sentinel3/service.key"], check=True)
    subprocess.run(["chown", "root:root", "/home/sentinel3/service.key"], check=True)
    os.chmod("/home/sentinel3/service.key", 0o400)
    write("sentinel3", "certificate-ledger.txt", "Service: ops.northstar.training\nIssuer: Northstar Training Test CA\nRevocation: clear in training-ca.crl\nKey permissions: /home/sentinel3/service.key is root:root mode 0400\nVerify offline with: openssl verify -attime 1893456000 -CAfile training-ca.pem -CRLfile training-ca.crl -crl_check service.pem\nSubmit service, issuer, revocation_status, and key_mode through `sentinel-submit`.\n")
    write("sentinel4", "exposure-review.conf", "Observed listener: ssh tcp/22\nConfigured default service: legacy-metrics disabled\nNo web, database, or remote-management service is exposed.\nSubmit listener, port, and legacy_metrics through `sentinel-submit`.\n")


if __name__ == "__main__":
    main()
