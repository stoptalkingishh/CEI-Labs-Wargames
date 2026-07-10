# Facilitation Runbook

How to actually run a live event on this platform — written for whoever
is in the room running it, who may not be whoever built it. Pairs with
`docs/instructor-cheatsheet.md` (level-by-level help) and
`docs/troubleshooting-faq.md` (known quirks, cross-linked from here
rather than duplicated).

## Before the event

1. **Deploy the stack** and confirm CTFd, the orchestrator, and all
   three tracks' images are reachable. Use the same verification
   discipline as this project's own build/deploy passes: don't assume a
   green deploy script means the stack actually works — launch one real
   instance per track and confirm you get back a real connect host/port,
   not just a 200.
2. **Create participant accounts** (or open registration) ahead of time
   so day-of time isn't spent on account creation. If using CTFd Teams
   mode, remember team membership must be set via
   `POST /api/v1/teams/<id>/members`, not by patching the user directly
   (see `docs/troubleshooting-faq.md`) — relevant if you're scripting
   bulk account setup rather than using the admin UI.
3. **Decide your release pace.** Track-level release-gating (letting you
   open Bandit/Krypton/Natas independently, at your own pace, based on
   how far participants have gotten) is a planned feature, not yet
   built — see the "Track release-gating" note in
   `docs/wargame-building-playbook.md`. Until it exists, all three
   tracks are visible as soon as challenges are synced; plan your event
   structure (e.g., a fixed schedule, or manually hiding/unhiding
   individual challenges via the CTFd admin UI) around that constraint.
4. **Print or pull up** `docs/instructor-cheatsheet.md` — that's your
   fast-lookup reference while walking the room.

## During the event

- **Point stuck participants at the in-platform hints first.** All 56
  levels have 3-tier hints (bare pointer → concept explanation → full
  walkthrough), deliberately costed so using them has a real trade-off.
  The cheat sheet is for *you*, to unstick someone faster than reading a
  hint stub yourself — not something to hand to a participant directly.
- **Natas participants need the attacker workstation**, not a direct
  connection — every Natas target is reachable only from inside it.
  Point people at noVNC first (no credential needed, works in-browser);
  see the FAQ entry on attacker-workstation access before troubleshooting
  a "can't log in" report as if it were a bug.
- **Shared-box tracks (Bandit, Krypton):** everyone on a track shares one
  persistent target box. If something looks broken in a way the puzzle
  itself doesn't explain, try **Reboot Host** from that participant's
  launch panel before assuming it's a platform bug — this resets the box
  in place without losing progress.
- **If a launch looks stuck or a status check flickers** (shows "not
  started" right after a participant says they clicked Launch), don't
  immediately treat it as broken — this matches a known orchestrator
  race (see FAQ). Have them refresh or re-check status once; it
  self-resolves. If it doesn't resolve after a couple of tries, that's
  worth escalating for a real look, not just retrying indefinitely.
- **Watch the scoreboard** (CTFd's own, no custom tooling needed) to see
  which tracks/levels are causing pileups — useful signal for whether to
  nudge everyone toward a hint, extend time, or just let people work
  through it.

## If something breaks

Distilled "if X, do Y" list, expanded with full technical detail in
`docs/troubleshooting-faq.md` and the underlying status docs it links
to:

| Symptom | Likely cause | Do this |
|---|---|---|
| Launch status flickers between "up" and "not started" right after launching | Orchestrator's 2-worker in-memory state race — see FAQ | Refresh/retry the status check once or twice; don't relaunch |
| Two different challenges' instances collide or one won't come up | Same race, port-allocation edge | Wait a few seconds and retry the launch; if it persists, flag for a restart of the orchestrator |
| A participant reports "reboot/relaunch/extend returns an error" | Possibly the documented Swarm network-recreation race on relaunch | Retry the same relaunch once — this specific race is known non-deterministic and typically succeeds on retry |
| An admin content-sync script gets 403s on delete calls | CTFd's CSRF check quirk on bodyless DELETEs — see FAQ | Not participant-facing; if you're running sync scripts yourself, add `Content-Type: application/json` to DELETE calls |
| Natas participant can't SSH into the attacker workstation | No credential is surfaced anywhere in the UI — see FAQ | Direct them to noVNC instead (password-free); this is a known gap, not something to debug further live |
| Orchestrator was restarted mid-event and now reports state that doesn't match reality | In-memory store has no reconciliation against real Docker state | Needs manual cleanup (remove orphaned services/networks by name) — plan to avoid restarting the orchestrator mid-event |

## After the event

- Pull the CTFd scoreboard/submission export if you want a record —
  standard CTFd admin functionality, nothing custom here.
- If you hit anything not covered above, add it to
  `docs/troubleshooting-faq.md` so the next event benefits — this
  runbook and the FAQ are meant to keep growing with real usage, the
  same way the hint content and writeups did during development.
