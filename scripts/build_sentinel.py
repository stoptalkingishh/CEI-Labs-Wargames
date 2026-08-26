"""Build the non-staged Sentinel foundations and deferred expansion labs."""

import json
import os

try:
    from hint_economy import managed_tiers
except ModuleNotFoundError:
    from scripts.hint_economy import managed_tiers

SENTINEL_IMAGE = os.environ.get(
    "SENTINEL_IMAGE", "ghcr.io/stoptalkingishh/cei-labs-wargames/sentinel-target:latest"
)
INSTANCE_GROUP = "sentinel"
DEFERRED_EXPANSION_STATUS = "This is a non-staged, offline Sentinel expansion lab. Labs 06-21 remain planned."


def _dynamic(key):
    return {"type": "per_team_dynamic", "content": "per-team-dynamic (placeholder, not read)", "data": key}


def _flags_yaml(flag):
    return (
        f'  - type: {flag["type"]}\n'
        f'    content: "{flag["content"]}"\n'
        f'    data: "{flag["data"]}"\n'
    )


challenges_data = [
    {"id": "sentinel-start-here", "name": "Sentinel: Start Here", "points": 10,
     "goal": "Connect safely to the Northstar operations jump host and retrieve your onboarding token.",
     "task": "Launch the environment and sign in as `sentinel0` with the public starter password `sentinel0`. Read `~/evidence/ENGAGEMENT-RULES.txt` and submit the documented structured answer through `sentinel-submit`.",
     "flag": _dynamic("sentinel-start-here")},
    {"id": "sentinel-01", "name": "Sentinel 01: Asset Census", "points": 200,
     "goal": "Reconcile a supplied asset inventory with the host's installed software, active services, and ownership evidence.",
     "task": "Work as `sentinel0`. Review the local inventory evidence and submit the documented structured evidence tuple through `sentinel-submit`.", "flag": _dynamic("sentinel-01")},
    {"id": "sentinel-02", "name": "Sentinel 02: Control Review", "points": 250,
     "goal": "Classify the safeguards documented on the host by their control category and purpose.",
     "task": "Work as `sentinel1`. Compare the control statements with their evidence and submit the documented structured classification tuple through `sentinel-submit`.", "flag": _dynamic("sentinel-02")},
    {"id": "sentinel-03", "name": "Sentinel 03: Change Window", "points": 300,
     "goal": "Review a change request for approval, testing, and rollback evidence before selecting the safe action.",
     "task": "Work as `sentinel2`. Inspect the local change packet and submit the documented disposition and missing-evidence tuple through `sentinel-submit`.", "flag": _dynamic("sentinel-03")},
    {"id": "sentinel-04", "name": "Sentinel 04: Certificate Trail", "points": 350,
     "goal": "Trace certificate, key-permission, and revocation evidence to identify the trustworthy service identity.",
     "task": "Work as `sentinel3`. Inspect the certificate evidence package and submit the documented structured evidence tuple through `sentinel-submit`.", "flag": _dynamic("sentinel-04")},
    {"id": "sentinel-05", "name": "Sentinel 05: Attack Surface", "points": 400,
      "goal": "Enumerate the host's listening services and review configuration artifacts to identify the exposed default service.",
      "task": "Work as `sentinel4`. Review the local exposure evidence and submit the documented structured exposure tuple through `sentinel-submit`.", "flag": _dynamic("sentinel-05")},
    {"id": "sentinel-22", "name": "Sentinel 22: Phishing Header Analysis", "points": 450,
     "goal": "Identify the sender-path inconsistency in a supplied synthetic email from its authentication and Received headers.",
     "task": "Work as `sentinel22`. Review only the static local file `~/evidence/phishing-message.eml`; do not contact mail systems or services. Submit the documented structured header-analysis tuple through `sentinel-submit`. " + DEFERRED_EXPANSION_STATUS, "flag": _dynamic("sentinel-22")},
    {"id": "sentinel-23", "name": "Sentinel 23: Detection Rule Validation", "points": 475,
     "goal": "Validate a fixed detection rule against a committed local log corpus and interpret its decision record.",
     "task": "Work as `sentinel23`. Review only the static local rule, log corpus, and decision record in `~/evidence/`; do not query live services. Submit the documented structured rule-validation tuple through `sentinel-submit`. " + DEFERRED_EXPANSION_STATUS, "flag": _dynamic("sentinel-23")},
    {"id": "sentinel-24", "name": "Sentinel 24: Endpoint Enrollment Evidence", "points": 500,
     "goal": "Confirm endpoint enrollment from a simulated local transcript, key lifecycle record, and inventory entry.",
     "task": "Work as `sentinel24`. Review only the static local file `~/evidence/endpoint-enrollment.txt`; do not contact an endpoint, agent, or manager. Submit the documented structured enrollment tuple through `sentinel-submit`. " + DEFERRED_EXPANSION_STATUS, "flag": _dynamic("sentinel-24")},
    {"id": "sentinel-25", "name": "Sentinel 25: Alert Triage Summary", "points": 525,
     "goal": "Identify the evidence-supported root cause by corroborating a deterministic local alert summary with its fixed certificate inventory record.",
     "task": "Work as `sentinel25`. Review only the static local files `~/evidence/alert-triage-summary.txt` and `~/evidence/vpn-certificate-inventory.txt`; do not use an external AI service or contact systems. Submit the documented structured triage-summary tuple through `sentinel-submit`. " + DEFERRED_EXPANSION_STATUS, "flag": _dynamic("sentinel-25")},
    {"id": "sentinel-26", "name": "Sentinel 26: Network Inventory Review", "points": 550,
     "goal": "Identify the unauthorized synthetic device from static ARP/DHCP inventory and network-zone policy evidence.",
     "task": "Work as `sentinel26`. Review only the static local file `~/evidence/network-inventory.txt`; do not scan networks or contact external services. Submit the documented structured inventory-review tuple through `sentinel-submit`. " + DEFERRED_EXPANSION_STATUS, "flag": _dynamic("sentinel-26")},
    {"id": "sentinel-27", "name": "Sentinel 27: Evidence Metadata Review", "points": 575,
     "goal": "Review a bounded extraction from an original local document fixture with its metadata and checksum.",
     "task": "Work as `sentinel27`. Review only the static local file `~/evidence/evidence-metadata.txt`; do not upload, transmit, or enrich the fixture with external tools. Submit the documented structured metadata-review tuple through `sentinel-submit`. " + DEFERRED_EXPANSION_STATUS, "flag": _dynamic("sentinel-27")},
]

HINTS = {
    "sentinel-01": ["Start with the supplied inventory, then independently inspect what this host reports.", "Compare package, service, and ownership fields rather than relying on a single source.", "Use `dpkg -l`, `pgrep -a sshd`, and `stat` on the named evidence files; submit the documented evidence tuple through `sentinel-submit`."],
    "sentinel-02": ["Each statement describes a safeguard and an intended outcome.", "Control categories include technical, administrative, and physical; purposes include preventive, detective, and corrective.", "Read `controls.md` and `control-evidence.md`, then submit the documented MFA, badge-review, and log-review classification tuple through `sentinel-submit`."],
    "sentinel-03": ["A safe production change has accountable approval, testing evidence, and a viable rollback.", "Read every section of the change packet before deciding whether the requested window should proceed.", "Submit the documented `disposition` and `missing_evidence` tuple through `sentinel-submit`."],
    "sentinel-04": ["Trust requires more than a familiar subject name.", "Compare issuer, validity, offline revocation status, and private-key permissions across the provided records.", "Use the fixed-time `openssl verify` command in the ledger and `stat -c '%a %U:%G' service.key`, then submit the evidence tuple through `sentinel-submit`."],
    "sentinel-05": ["Observed listeners and intended configuration are separate sources of evidence.", "Enumerate TCP listeners, then compare them with the exposure review and service configuration.", "Use `ss -lnt` and read `exposure-review.conf`, then submit the documented listener, port, and legacy-metrics tuple through `sentinel-submit`."],
    "sentinel-22": ["Compare the visible sender with the envelope sender and authentication results.", "The RFC-822 message is synthetic static evidence; do not contact a mail system or inspect a live mailbox.", "An SPF pass for the envelope sender does not establish alignment with the visible From domain; record the from_domain, return_path_domain, and dmarc values from `phishing-message.eml` through `sentinel-submit`."],
    "sentinel-23": ["The decision record identifies the fixed rule and the corpus result it produced.", "The supplied rule and log corpus are committed static evidence, not a prompt to run a live detection service.", "Read `detection-rule.yml`, `detection-corpus.log`, and `decision-record.txt`, then submit the rule_id, matches, and decision tuple through `sentinel-submit`."],
    "sentinel-24": ["Enrollment is supported only when the transcript, key lifecycle, and inventory agree.", "This simulated record is static evidence only: do not contact an endpoint, agent, or manager.", "Read `endpoint-enrollment.txt`, then submit the endpoint_id, enrollment_status, and key_status tuple through `sentinel-submit`."],
    "sentinel-25": ["Treat the deterministic summary as an index and corroborate its root-cause claim with the referenced certificate inventory record.", "Use only the two fixed local evidence files; do not use an external AI service or contact a live system.", "Read `alert-triage-summary.txt` and `vpn-certificate-inventory.txt`, then submit the alert_id, root_cause, and disposition tuple through `sentinel-submit`."],
    "sentinel-26": ["Compare the static ARP and DHCP observations with the network-zone policy before identifying the device.", "The inventory is synthetic evidence only: do not scan a network, probe a device, or contact an external service.", "Read `network-inventory.txt`, then submit the device_mac, zone, and disposition tuple through `sentinel-submit`."],
    "sentinel-27": ["Use the supplied metadata and checksum to review the bounded extraction from the original fixture.", "Keep the fixture local: do not upload, transmit, or use external enrichment tools.", "Run `sha256sum ~/evidence/field-notes.pdf`, compare it with `evidence-metadata.txt`, then submit the filename, sha256, and extracted_author tuple through `sentinel-submit`."],
}


def validate():
    ids = [challenge["id"] for challenge in challenges_data]
    expected_ids = ["sentinel-start-here", *[f"sentinel-{number:02d}" for number in range(1, 6)], *[f"sentinel-{number}" for number in range(22, 28)]]
    if ids != expected_ids or len(set(ids)) != len(ids):
        raise ValueError("Sentinel must contain the pilot and deferred labs 22-27 exactly once")
    if set(HINTS) != set(ids) - {"sentinel-start-here"}:
        raise ValueError("only scored Sentinel labs may have managed hints")
    for challenge in challenges_data:
        if challenge["id"] in HINTS:
            managed_tiers(challenge["points"], HINTS[challenge["id"]])
        if "hint" in challenge["task"].lower():
            raise ValueError("descriptions must not disclose hint-tier solutions")


def build(base_dir):
    validate()
    os.makedirs(base_dir, exist_ok=True)
    for challenge in challenges_data:
        path = os.path.join(base_dir, challenge["id"])
        os.makedirs(path, exist_ok=True)
        description = f"## Goal\n{challenge['goal']}\n\n---\n\n### The task\n{challenge['task']}\n"
        escaped = "\n".join(("  " + line) if line and index else line for index, line in enumerate(description.splitlines()))
        content = f'''name: "{challenge["name"]}"
author: "CEI Labs"
category: "Security Operations"
description: |
  {escaped}
value: {challenge["points"]}
type: standard
flags:
{_flags_yaml(challenge["flag"])}state: hidden
version: "0.1"
instance_type: single-target
image: {SENTINEL_IMAGE}
instance_group: {INSTANCE_GROUP}
shutdown_on_solve: false
show_launcher: {str(challenge["id"] == "sentinel-start-here").lower()}
'''
        with open(os.path.join(path, "challenge.yml"), "w", encoding="utf-8") as output:
            output.write(content)
    entries = [{"name": challenge["name"], "tiers": [{"tier": tier, "cost": cost, "content": text} for tier, (text, cost) in enumerate(managed_tiers(challenge["points"], HINTS[challenge["id"]]), 1)]} for challenge in challenges_data if challenge["id"] in HINTS]
    with open(os.path.join(base_dir, "sentinel-hint-wallet.json"), "w", encoding="utf-8") as output:
        json.dump({"schema_version": 1, "track": "sentinel", "entries": entries}, output)


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    build(os.path.join(root, "challenges"))
