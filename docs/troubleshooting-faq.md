# Troubleshooting / Known-Issues FAQ

Consolidated, lookup-friendly version of the known-limitations found
during development and playtesting. Each entry links back to the fuller
technical write-up in the relevant status doc rather than duplicating
it — check there for the full diagnosis if the short version here isn't
enough.

Full technical detail lives in:
- `cei-labs-engine/docs/self-hosted-wargames-status.md`
- `CEI-Labs-Wargames/docs/self-hosted-wargames-status.md`
- `cei-labs-engine/docs/hint-tier-persona-findings.md`

---

**Q: A participant's launch status flickers between "up" and "not
started" right after they click Launch. Is their environment actually
broken?**
No. The orchestrator runs as 2 separate worker processes with
independent in-memory state (no shared store, no Redis) — a status
check has a real chance of landing on the worker that hasn't seen the
launch yet, so it briefly reports "not started" even though the
environment is genuinely up. Refreshing the status check resolves it.
See "Critical finding: the orchestrator's in-memory state isn't
actually shared" in `cei-labs-engine/docs/self-hosted-wargames-status.md`.

**Q: Two challenges launched close together seem to collide (port
conflict, or one instance never comes up).**
Same root cause as above — the 2-worker race can let two near-
simultaneous launches both think a port is free. Wait a few seconds and
retry the launch. Not fixed as of this writing; treat it as a known,
higher-priority-but-not-yet-addressed platform limitation, not something
to debug per-incident.

**Q: Reboot/Relaunch/Extend occasionally returns a 500 with a network
error.**
`relaunch` specifically can hit a real Docker Swarm eventual-consistency
race: the old network is torn down and a new one created in the same
request, and Swarm's control plane doesn't always finish removing the
old one before the new one is created, causing the following service
creation to fail. Confirmed non-deterministic — an immediate retry of
the same action succeeds. Not fixed; see "Known open items" in
`cei-labs-engine/docs/self-hosted-wargames-status.md`.

**Q: How does a Natas participant log into the shared attacker
workstation?**
Use **noVNC** (the browser-desktop link on the launch panel) — it needs
no credential from the participant's side. SSH is also offered as an
option, but its login credential (`operator` / a build-time secret) is
not currently surfaced anywhere in the launch panel UI or its API
responses — a real gap, not something participants are meant to
puzzle out. Point everyone at noVNC first; treat "I can't SSH into the
attacker" reports as expected, not a bug to chase, until this is fixed
platform-side.

**Q: The launch panel used to show a full explanatory paragraph and a
pre-filled `ssh operator@...` line — now it just shows Host/Port. Is
that intentional?**
Yes — real playtest feedback found the extra prose added noise (and the
pre-filled username was wrong for most levels anyway). The panel is now
deliberately minimal: Host/Port only (plus, for Natas, the attacker
links and target hostname). See "Player-experience round 2" in
`cei-labs-engine/docs/self-hosted-wargames-status.md`.

**Q: Why don't all 34 Bandit levels show their own Launch button
anymore?**
Intentional — a shared-box track only needs to be launched once. Only
each track's "Start Here" challenge shows the launcher by default now
(`InstanceChallengeConfig.show_launcher`); every other level in that
group hides it to cut clutter. If a deployment predates this change, it
needs a manual `ALTER TABLE ... ADD COLUMN show_launcher BOOLEAN NOT
NULL DEFAULT TRUE` migration — see the same status doc section.

**Q: An admin content-sync script gets a 403 on hint/challenge DELETE
calls even though the CSRF token looks correct.**
CTFd's CSRF check only validates the `CSRF-Token` header when the
request's `Content-Type` is exactly `application/json`. A bodyless
DELETE has no `Content-Type` by default, so it silently falls through to
a form-nonce check a header-only script never satisfies. Fix: always set
`Content-Type: application/json` explicitly on DELETE calls, even with
an empty body. Not a CTFd bug or a real permissions gap — purely a
client-script detail, and not participant-facing.

**Q: The orchestrator was restarted (or something was manually changed
in Docker) and now its reported state doesn't match reality.**
Expected — the orchestrator's instance/range state is a pure in-memory
dict with no reconciliation against actual Docker/Swarm state. Restarts
or out-of-band Docker changes leave it either reporting instances that
no longer exist, or believing ports are free that are still bound.
Workaround: manually remove the orphaned service/network by exact name
and let a fresh request recreate it in sync. Avoid restarting the
orchestrator process mid-event if at all possible.

**Q: A hint or description looks like it doesn't quite match what
actually happens on the target.**
This did happen at least twice during development (documented and fixed
— see `cei-labs-engine/docs/hint-tier-persona-findings.md` and the
verification notes in `CEI-Labs-Wargames/docs/writeups/`), so it's worth
taking seriously rather than assuming participant error. If you confirm
a real mismatch during a live event, note the exact command/output and
file it the same way — the goal is for the writeups and hints to stay
accurate as the source of truth, not just the target images.
