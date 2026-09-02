# Krypton — Instructor Cheat Sheet

Fast-lookup reference for walking a room during a live session. One row
per level: what it's testing, the one-line nudge to give someone who's
stuck, and the core technique in a few words. Not a substitute for the
full writeup (`writeups.md`, same folder) — if a one-liner doesn't
unstick someone, jump to the matching writeup section (same level name)
for the complete explanation.

Every level's own in-platform hints (3 tiers, point-costed) are the
first thing to point a stuck participant at — this sheet is for when
you're walking the room and need the answer in your own head *faster*
than reading a hint stub yourself, or when someone's stuck in a way the
hints don't quite address (e.g., a terminal/environment issue, not a
puzzle issue).

Shared box, SSH — everyone on the track shares one persistent target.
If a participant's session looks broken in a way not explained by the
puzzle itself, a **Reboot Host** from the launch panel is the first
thing to try before assuming it's a real bug.

| Level | Goal | If they're stuck, point them at... | Core technique |
|---|---|---|---|
| 0→1 | Base64 | "Same as Bandit 10 — what decodes Base64?" | `base64 -d` |
| 1→2 | ROT13 | "Self-inverse rotation — same command decodes as encodes." | `tr` rotation |
| 2→3 | Unknown Caesar shift | "You have a tool that encrypts with the same key — feed it something predictable and see what comes out." | probe with known plaintext (`AAAA...`), derive shift, reverse it |
| 3→4 | Frequency analysis | "English letters aren't evenly distributed — count letter frequency and match against the standard order." | letter-frequency count vs. E-T-A-O-I-N... |
| 4→5 | Vigenère, known key length | "Split the ciphertext into N interleaved groups by key length — each group alone is just a Caesar shift." | column split, per-column frequency analysis |
| 5→6 | Vigenère, unknown key length | "Find repeated chunks in the ciphertext and look at the *distance* between repeats — that reveals the key length." | Kasiski examination, then level 4's technique |
| 6→7 | Stream cipher (final) | "Feed the encryptor a long run of one known character — the output directly reveals the repeating keystream." | known-plaintext keystream recovery, XOR/subtract to decrypt |
