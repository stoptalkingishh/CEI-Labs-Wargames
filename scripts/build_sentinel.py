"""Build the non-staged Sentinel foundations pilot challenge definitions."""

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
     "task": "Launch the environment and sign in as `sentinel0` with the public starter password `sentinel0`. Read the engagement rules in your home directory and submit the onboarding token.",
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
]

HINTS = {
    "sentinel-01": ["Start with the supplied inventory, then independently inspect what this host reports.", "Compare package, service, and ownership fields rather than relying on a single source.", "Use `dpkg -l`, `pgrep -a sshd`, and `stat` on the named evidence files; submit the documented evidence tuple through `sentinel-submit`."],
    "sentinel-02": ["Each statement describes a safeguard and an intended outcome.", "Control categories include technical, administrative, and physical; purposes include preventive, detective, and corrective.", "Read `controls.md` and `control-evidence.md`, then submit the documented MFA, badge-review, and log-review classification tuple through `sentinel-submit`."],
    "sentinel-03": ["A safe production change has accountable approval, testing evidence, and a viable rollback.", "Read every section of the change packet before deciding whether the requested window should proceed.", "Submit the documented `disposition` and `missing_evidence` tuple through `sentinel-submit`."],
    "sentinel-04": ["Trust requires more than a familiar subject name.", "Compare issuer, validity, offline revocation status, and private-key permissions across the provided records.", "Use the fixed-time `openssl verify` command in the ledger and `stat -c '%a %U:%G' service.key`, then submit the evidence tuple through `sentinel-submit`."],
    "sentinel-05": ["Observed listeners and intended configuration are separate sources of evidence.", "Enumerate TCP listeners, then compare them with the exposure review and service configuration.", "Use `ss -lnt` and read `exposure-review.conf`, then submit the documented listener, port, and legacy-metrics tuple through `sentinel-submit`."],
}


def validate():
    ids = [challenge["id"] for challenge in challenges_data]
    if len(ids) != 6 or len(set(ids)) != 6:
        raise ValueError("Sentinel pilot must contain exactly six unique challenges")
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
