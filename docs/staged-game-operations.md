# Staged Game Operations

This runbook governs live use of the administrator-started game stages defined
by `game-stages.yml`. It complements the static manifest contract in
`docs/staggered-game-stages.md`; Engine/CTFd owns stage state, timestamps,
scoreboards, and audit records.

## Operating model

Each game is started independently. Starting a later game does not change an
earlier game's state: it may remain active, be locked for scoring, or have its
scoreboard hidden at the event lead's direction. A break in the schedule is not
an automatic stage transition.

Each stage has its own zero time. Stage awards use that game's scoreboard and
the approved tie-break policy, not the stock overall CTFd scoreboard.

## Roles

- **Event lead:** authorizes starts, scoring cutoffs, and incident decisions.
- **Stage operator:** performs stage actions in CTFd and announces each action
  immediately before taking it.
- **Scoring verifier:** independently records UTC times, checks the
  participant view, and preserves result evidence.
- **Communications lead:** gives participant countdowns and explains whether a
  break affects scoring.

The stage operator and scoring verifier must be different people during a
rehearsal and a live event.

## Preflight

1. Record the immutable Engine, Wargames, and event configuration references.
2. Generate the catalog and run `python3 scripts/validate_game_stages.py`.
   Its expected counts are authoritative; do not copy them into this runbook.
3. Sync mappings in Engine/CTFd and reconcile the sync report with the stage
   manifest before any game starts.
4. Confirm every stage is pending, stage scoreboards are hidden, and a clean
   participant account cannot access scored-game content.
5. Confirm host and CTFd clocks are synchronized; record the UTC source and
   observed offset.
6. Back up CTFd/MariaDB, begin the incident log, and open monitoring.
7. From a clean participant account, verify login, the participant quick-start,
   and each track's Start Here path.

Do not start a game with a mapping-count warning, failed backup, clock issue,
or unresolved scoring discrepancy.

## Start, break, and close

### Starting a game

1. The event lead authorizes the named game to start.
2. Communications gives a visible or audible countdown and directs players to
   that track's Start Here challenge.
3. The operator presses Start once.
4. The verifier records the displayed UTC `started_at`, confirms the
   scoreboard visibility, and confirms that only the intended stage opened.
5. Two test participants complete a controlled smoke solve and the verifier
   checks that elapsed time is measured from this stage's start.

### Breaks and visibility

- Leave a stage active if its scoring continues through a break.
- Lock a stage only when the event lead authorizes a cutoff. Learning access
  may remain available while later solves cease to affect its standings.
- Hide or show a scoreboard only for presentation, suspense, or investigation;
  visibility must not change scoring data.

### Locking and closing

- **Lock:** preserve the scoring cutoff and verify a post-cutoff controlled
  solve does not change the stage standings.
- **Close:** complete reconciliation after the cutoff. If closing directly from
  active is supported, its timestamp is the cutoff.
- Never delete challenges, mappings, submissions, or database rows to resolve
  an event-day discrepancy.

## Incident response

If Start appears to fail, do not retry blindly. Capture the participant and
administrator view, UTC time, CTFd logs, and audit rows; refresh and inspect
the immutable start timestamp. If standings appear wrong, hide the affected
scoreboard when appropriate, preserve the database and raw solves, and escalate
to the event lead. Manual adjudication requires a written rationale, affected
accounts, evidence, two-person approval, and a preserved pre-change export.

## Evidence and rehearsal

For every stage retain the release references, manifest-validation output,
mapping report, start/lock/close UTC times, audit entries, participant and
administrator screenshots, raw solves, final standings export, monitoring
snapshots, and all incident decisions.

The dress rehearsal must use multiple participant accounts and overlap at least
two active stages. Test starts, hide/show, locks, scoreboard polling, and solve
bursts at stage boundaries. Pass only when timestamps are immutable, mappings
do not leak across stages, valid in-window solves are included, post-lock scores
do not change, and infrastructure remains within its approved capacity budget.
