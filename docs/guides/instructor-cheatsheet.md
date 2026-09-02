# Instructor Cheat Sheet

Fast-lookup reference for walking a room during a live session. Each
track has its own cheat sheet, in its own folder alongside that track's
full writeups and learning objectives:

- [`Bandit cheatsheet`](../tracks/bandit/cheatsheet.md)
- [`Krypton cheatsheet`](../tracks/krypton/cheatsheet.md)
- [`Natas cheatsheet`](../tracks/natas/cheatsheet.md)

Every level's own in-platform hints (3 tiers, point-costed) are the
first thing to point a stuck participant at — these sheets are for when
you're walking the room and need the answer in your own head *faster*
than reading a hint stub yourself, or when someone's stuck in a way the
hints don't quite address (e.g., a terminal/environment issue, not a
puzzle issue).

## Notes for facilitators

- **Point-cost hints vs. these sheets:** encourage participants to use
  the platform's own hints first — they're built to cost points on
  purpose (see `wargame-building-playbook.md`). These sheets are for
  you, not for handing directly to a stuck participant.
- **Natas attacker workstation access:** after the event operator has
  completed the release checks in `natas-completion-status.md`, noVNC is
  supported without a participant credential. SSH is unavailable unless
  the operator explicitly supplies and tests a specific endpoint and credential;
  point participants to noVNC first.
- **Shared-box tracks (Bandit, Krypton):** everyone on a track shares one
  target box. If a participant's session looks broken in a way not
  explained by the puzzle itself, a **Reboot Host** from the launch panel
  is the first thing to try before assuming it's a real bug.
