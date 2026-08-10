# Challenge hint links require live internet access (2026-07-24)

Reported: challenge descriptions/hints in CEI-Labs-Wargames still contain
live `https://` links to external sites, which conflicts with running the
event with no internet access. Notes only, no code changed.

## Confirmed scope

Source is `CEI-Labs-Wargames/scripts/build_{bandit,krypton,natas}.py`
(`challenges/*/challenge.yml` is generated output, gitignored — not
hand-edited, per repo convention). Checked against current `main`
(`f4d9291`):

- **40 URL occurrences** across the three build scripts, in two forms:
  - `EXTRA_INFO`/equivalent dicts feeding a "**Helpful reading:**" section
    rendered into the challenge description (`_render_description()` in
    each script) — e.g. `("ROT13 on Wikipedia", "https://en.wikipedia.org/wiki/ROT13")`.
  - Inline markdown links embedded directly in tier-1 hint text, e.g.
    `"[Setuid on Wikipedia](https://en.wikipedia.org/wiki/Setuid)."` —
    for a few levels (bandit-19 among them) this link **is** the entire
    tier-1 hint, not just a reference alongside other content.
- Five external domains total: `en.wikipedia.org`, `git-scm.com`,
  `help.ubuntu.com`, `jwiegley.github.io`, `linux.die.net`.
- Separately, `http://<target-host>:PORT/` strings throughout
  `build_natas.py` are **not** part of this issue — those are placeholders
  for the player's own local target box, not external destinations.

## This was already investigated once and explicitly accepted — worth knowing before re-deciding it

`CEI-Labs-Wargames/docs/offline-dependency-audit.md` (§2) already found
this exact set of 40 URLs / 5 domains and concluded it was **not** a gap:
reasoning given was that `cei-labs-net/docs/network-access.md` already
allowlists outbound WAN with a QoS priority exception for exactly these
five domains, so the player VLAN was deliberately designed to permit this
one narrow case of internet access. That audit explicitly frames the links
as optional "free hint" content, never required to solve a level (all
flags/passwords are derivable from content already inside the target box
per that same audit).

This request overrides that prior decision in favor of a stricter
zero-internet requirement. Flagging the conflict here rather than silently
picking a side — whoever implements this should also decide whether
`cei-labs-net`'s WAN allowlist/QoS exception for these five domains should
be removed too, since it exists specifically to support this now-rejected
design.

## Why this needs a real decision, not a mechanical fix

The literal request — "these should be cached web links" — runs into a
hard constraint: reproducing full third-party page content (Wikipedia
articles, git-scm.com's book, help.ubuntu.com's wiki, a personal GitHub
Pages site) as locally-hosted cached copies means copying substantial
amounts of someone else's copyrighted/licensed text into this repo and
event infrastructure. That's not something to do as a mechanical find/
replace — it needs an explicit decision on approach. Options, roughly
ordered by effort:

1. **Drop the links, keep the reference title as plain text** (e.g. "ROT13
   on Wikipedia." with no URL). Cheapest, fully removes the internet
   dependency, but for levels where the link *is* the hint (bandit-19's
   tier 1), this leaves a title with no actual content — a real
   degradation for those specific hints, not just a link removed.
2. **Write original, locally-authored explanations** to replace each link
   — e.g. a short paragraph explaining ROT13 or setuid in the repo's own
   words, instead of pointing at Wikipedia. No copyright concern since
   it's original content, but it's real writing work across ~15 distinct
   topics, and needs someone to actually verify technical accuracy per
   topic.
3. **License-compliant mirroring** — some of this content (Wikipedia in
   particular) is CC-BY-SA, which permits mirroring with proper
   attribution under the same license, unlike straightforwardly copying
   git-scm.com's book or a personal GitHub Pages site. This is the most
   faithful to "cached web links" but adds real scope: per-source
   attribution/licensing review, a hosting location (static assets served
   from CTFd itself? baked into the target images?), and a process to keep
   the mirror from silently going stale.

## What's needed before implementation

- A decision on which of the three options above (or a mix — e.g. option 1
  for pure "further reading" links, option 2 for the handful where the
  link is the actual hint content).
- A decision on `cei-labs-net`'s matching WAN/QoS allowlist for these five
  domains — keep it (defense in depth / participants who bring their own
  devices) or remove it now that the CTFd-side content no longer needs it.
- If mirroring (option 3) is chosen: a hosting location and an owner for
  keeping it current as `build_bandit.py`/`build_krypton.py`/
  `build_natas.py` change over time.
