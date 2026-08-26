# Krypton hints cross-reference against mayadevbe.me (2026-07-24)

Same exercise as the Bandit cross-reference (PRs #13, #14), applied to
Krypton. Fetched `https://mayadevbe.me/posts/overthewire/krypton/level0/`
through `level5/` (6 pages) and compared against `HINTS` in
`CEI-Labs-Wargames/scripts/build_krypton.py`. Notes only, no code
changed.

## Numbering

Our `krypton-NN` ids map directly to the site's `levelN` pages -- both
use the same "level N is a pure base64 decode with no shift/key"
starting point (`krypton-00` / site `level0`), so there's no offset
issue here the way there was for Bandit's late-game levels.

## Site's solve approach per level (as fetched 2026-07-24)

| Level | Site's approach |
|---|---|
| krypton-00 | `echo '<b64>' \| base64 -d` |
| krypton-01 | `tr 'A-Za-z' 'N-ZA-Mn-za-m'` (ROT13 self-inverse) |
| krypton-02 | Known-plaintext: encrypt `AAAAA`, observe shift from output, apply that shift with `tr` |
| krypton-03 | Frequency analysis on 3 combined intercepted files, map to standard English letter-frequency order, decrypt with `tr` |
| krypton-04 | **Paste ciphertext into `dcode.fr`'s Vigenere tool**, select "knowing the key-length" (6), retrieve the key, then decrypt the real ciphertext on the same external site |
| krypton-05 | Kasiski examination to find candidate key lengths (3/6/9), then break each with a Vigenere solver until English emerges |

## Comparison against our `HINTS` dict

Levels 00-03 and 05 line up closely -- same techniques, same
command-line tools (`tr`, `base64`), similar explanatory depth. Our
`HINTS["krypton-03"]` tier 3 is notably more mechanical/self-contained
than the site's version: it gives an exact `tr`/`fold`/`sort`/`uniq -c`
pipeline for the frequency count, where the site describes the
technique but leans on manual counting.

## The one real divergence: krypton-04 relies on an external website

The site's krypton-04 (Vigenere) walkthrough is solved almost entirely
by pasting ciphertext into `dcode.fr`, an external web-based cipher
tool -- not a local command. Our `HINTS["krypton-04"]` instead teaches
the underlying technique directly: split ciphertext into interleaved
groups by key length, solve each group's Caesar shift via the same
frequency-analysis method as krypton-03, then reassemble -- fully
offline, no external site involved.

This is not a gap to fix -- it's the opposite. `cei-labs-event`'s own
`docs/live-hint-links-offline-gap-2026-07-24.md` (from an earlier PR in
this series) already documents that this event's hint links must stay
resolvable without internet access. Porting the site's dcode.fr-based
approach into our krypton-04 hint would directly reintroduce that exact
already-flagged problem. Worth stating explicitly so nobody treats
"match the external walkthrough" as license to add an external-tool
dependency here.

## What closing this needs

- No hint-content changes appear justified by this comparison --
  krypton-00/01/02/03/05 already match or exceed the site's approach,
  and krypton-04 is correct to diverge (offline-first) rather than
  match.
- If anything, `HINTS["krypton-02"]`'s known-plaintext-attack framing
  and `HINTS["krypton-03"]`'s exact frequency-count pipeline could be
  used as reference examples of the "self-contained final command"
  quality bar when the earlier-flagged bandit-05 hint gets revisited.
