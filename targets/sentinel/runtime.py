#!/usr/bin/env python3
"""Render deterministic, per-team Sentinel evidence before sshd starts."""

import hashlib
import json
import os
import subprocess
import tempfile

KEYS = ("sentinel-start-here", "sentinel-01", "sentinel-02", "sentinel-03", "sentinel-04", "sentinel-05", "sentinel-22", "sentinel-23", "sentinel-24", "sentinel-25", "sentinel-26", "sentinel-27")
ACCOUNT_CREDENTIAL_KEYS = {
    "sentinel1": "sentinel-start-here",
    "sentinel2": "sentinel-01",
    "sentinel3": "sentinel-02",
    "sentinel4": "sentinel-03",
    "sentinel5": "sentinel-04",
    "sentinel22": "sentinel-22",
    "sentinel23": "sentinel-23",
    "sentinel24": "sentinel-24",
    "sentinel25": "sentinel-25",
    "sentinel26": "sentinel-26",
    "sentinel27": "sentinel-27",
}

ANSWERS = {
    "sentinel-start-here": {"engagement_scope": "local-evidence-only"},
    "sentinel-01": {"asset": "northstar-jump-01", "package": "openssh-server", "service": "sshd", "owner": "root:root"},
    "sentinel-02": {"mfa": "technical-preventive", "badge_review": "physical-preventive", "log_review": "technical-detective"},
    "sentinel-03": {"disposition": "DEFER", "missing_evidence": "change-owner-signature"},
    "sentinel-04": {"service": "ops.northstar.training", "issuer": "Northstar Training Test CA", "revocation_status": "clear", "key_mode": "0400"},
    "sentinel-05": {"listener": "ssh", "port": 22, "legacy_metrics": "disabled"},
    "sentinel-22": {"from_domain": "northstar.training", "return_path_domain": "invoice-notice.example", "dmarc": "fail"},
    "sentinel-23": {"rule_id": "NS-DET-104", "matches": 1, "decision": "triggered"},
    "sentinel-24": {"endpoint_id": "northstar-lt-042", "enrollment_status": "enrolled", "key_status": "active"},
    "sentinel-25": {"alert_id": "ALT-2048", "root_cause": "expired-vpn-certificate", "disposition": "close-benign"},
    "sentinel-26": {"device_mac": "02:00:00:00:26:01", "zone": "engineering", "disposition": "unauthorized"},
    "sentinel-27": {"filename": "field-notes.pdf", "sha256": "dc3014d5c2f708b7e4628082170c3c0385afbd6dd8d84f1aff0eca6d8abe7710", "extracted_author": "Northstar Training"},
}

LAB_26_EVIDENCE = (
    "Static synthetic network inventory\n"
    "ARP observation: 10.42.8.61 02:00:00:00:26:01\n"
    "DHCP registration: no lease for 02:00:00:00:26:01\n"
    "Network-zone policy: engineering permits only registered DHCP endpoints.\n"
    "Observed zone: engineering\n"
    "This is static evidence only. Do not scan or probe a network. "
    "Submit device_mac, zone, and disposition through `sentinel-submit`.\n"
)


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


def write_atomic(directory, name, text, mode):
    descriptor, temporary = tempfile.mkstemp(prefix=f".{name}.", dir=directory, text=True)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as output:
            output.write(text)
            os.fchown(output.fileno(), 0, 0)
        os.chmod(temporary, mode)
        os.replace(temporary, os.path.join(directory, name))
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def write(owner, name, text, mode=0o444):
    write_atomic(f"/srv/sentinel-evidence/{owner}", name, text, mode)


def write_root(name, text):
    write_atomic("/var/lib/sentinel", name, text, 0o600)


def main():
    secrets = load_secrets()
    for account, key in ACCOUNT_CREDENTIAL_KEYS.items():
        subprocess.run(["chpasswd"], input=f"{account}:{secrets[key]}\n", text=True, check=True)

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
    with open("/opt/sentinel/certs/service.key", encoding="utf-8") as source:
        write("sentinel3", "service.key", source.read(), 0o400)
    write("sentinel3", "certificate-ledger.txt", "Service: ops.northstar.training\nIssuer: Northstar Training Test CA\nRevocation: clear in training-ca.crl\nKey permissions: /srv/sentinel-evidence/sentinel3/service.key is root:root mode 0400\nVerify offline with: openssl verify -attime 1893456000 -CAfile training-ca.pem -CRLfile training-ca.crl -crl_check service.pem\nSubmit service, issuer, revocation_status, and key_mode through `sentinel-submit`.\n")
    write("sentinel4", "exposure-review.conf", "Observed listener: ssh tcp/22\nConfigured default service: legacy-metrics disabled\nNo web, database, or remote-management service is exposed.\nSubmit listener, port, and legacy_metrics through `sentinel-submit`.\n")
    write("sentinel22", "phishing-message.eml", "From: Northstar Billing <billing@northstar.training>\nReturn-Path: <reply@invoice-notice.example>\nAuthentication-Results: northstar.training; spf=pass smtp.mailfrom=invoice-notice.example; dkim=fail header.d=invoice-notice.example; dmarc=fail header.from=northstar.training\nReceived: from relay.invoice-notice.example (192.0.2.44) by mail.northstar.training with ESMTP\nSubject: Synthetic training invoice\n\nStatic synthetic RFC-822 training fixture. Do not contact mail systems.\nSubmit from_domain, return_path_domain, and dmarc through `sentinel-submit`.\n")
    write("sentinel23", "detection-rule.yml", "id: NS-DET-104\ntitle: Encoded PowerShell Command\ncondition: command_line contains '-EncodedCommand'\n")
    write("sentinel23", "detection-corpus.log", "2026-08-14T12:00:00Z host=lab-01 process=powershell.exe command_line='powershell.exe -EncodedCommand VwByAGkAdABlAC0ASABvAHMAdAAn\n")
    write("sentinel23", "decision-record.txt", "Static local rule-runner decision record\nRule: NS-DET-104\nMatches: 1\nDecision: triggered\nNo live detection service was queried. Submit rule_id, matches, and decision through `sentinel-submit`.\n")
    write("sentinel24", "endpoint-enrollment.txt", "Static simulated enrollment transcript\nEndpoint inventory ID: northstar-lt-042\nEnrollment transcript: accepted\nEnrollment status: enrolled\nEnrollment key lifecycle: active\nDo not contact an endpoint, agent, or manager. Submit endpoint_id, enrollment_status, and key_status through `sentinel-submit`.\n")
    write("sentinel25", "alert-triage-summary.txt", "Deterministic local alert summary\nAlert ID: ALT-2048\nSummary: VPN authentication failures followed certificate expiry; no anomalous source or privilege change is present.\nSource evidence: certificate inventory records the VPN certificate as expired.\nEvidence-supported root cause: expired-vpn-certificate\nDisposition: close-benign\nDo not use an external AI service or contact systems. Submit alert_id, root_cause, and disposition through `sentinel-submit`.\n")
    write("sentinel26", "network-inventory.txt", LAB_26_EVIDENCE)
    with open("/opt/sentinel/fixtures/field-notes.pdf", encoding="ascii") as source:
        write("sentinel27", "field-notes.pdf", source.read())
    write("sentinel27", "evidence-metadata.txt", "Original static local document fixture: field-notes.pdf\nSHA-256 (bounded fixture record): dc3014d5c2f708b7e4628082170c3c0385afbd6dd8d84f1aff0eca6d8abe7710\nMetadata author: Northstar Training\nBounded extraction result: training field notes\nDo not upload, transmit, or enrich this fixture externally. Submit filename, sha256, and extracted_author through `sentinel-submit`.\n")


if __name__ == "__main__":
    main()
