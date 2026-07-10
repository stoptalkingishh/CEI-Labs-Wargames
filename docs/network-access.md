# Required Network Access

Audience: whoever manages the network this platform runs on (see
[`cei-labs-net`](https://github.com/stoptalkingishh/cei-labs-net)), not
participants or instructors. This is the source-of-truth list of
external sites the wargame content links participants to, so the
network side can guarantee they're reachable.

## Why this exists

Every challenge's "Helpful reading" section (free, always-visible, part
of the 3-tier hint model — see `wargame-building-playbook.md`) links out
to a small, fixed set of external reference pages: Wikipedia articles
explaining a concept, and a handful of technical references for Git.
Player VLANs already default-allow outbound to WAN (see `cei-labs-net`'s
`docs/network-topology.md`), so these pages are reachable without any
change — but `cei-labs-net`'s QoS layer also runs App-ID/Zenarmor
signature-based traffic shaping that reclassifies bulk/update-like
traffic into a deliberately crippled 256 Kbit/s pipe (`docs/security-
qos-policy.md` §4.3). Without an explicit exception, a false-positive
match on one of these domains could throttle a participant reading a
hint's reference page mid-challenge with no obvious cause.

`cei-labs-net` maintains a `Wargame_Reference_Sites` firewall alias that
guarantees these specific hosts always get priority (`qInteractive`)
treatment, never the throttle pipe — see that repo's
`config/pfsense/wargame-reference-allowlist.xml` and
`docs/security-qos-policy.md` §4.4. **This document is the source of
truth that alias mirrors** — if this list changes, that alias needs the
same change.

## Required domains

| Domain | Used for |
|---|---|
| `en.wikipedia.org` | Concept background across all three tracks (see table below) |
| `git-scm.com` | Git installation instructions (Bandit's 5 git levels) |
| `help.ubuntu.com` | SSH key-based authentication reference (Bandit 13) |
| `jwiegley.github.io` | "Git from the Bottom Up" internals guide (Bandit's 5 git levels) |
| `linux.die.net` | Bash special-characters reference (Bandit 1) |

## Full link inventory, by level

Kept in sync with the `EXTRA_INFO` reading-link dicts in
`scripts/build_bandit.py`, `build_krypton.py`, `build_natas.py` — see
"Keeping this current" below for the audit command.

### Bandit

| Level | Link |
|---|---|
| 0→1 | [Secure Shell (SSH)](https://en.wikipedia.org/wiki/Secure_Shell) |
| 1→2 | [Advanced Bash-Scripting Guide — Special Characters](https://linux.die.net/abs-guide/special-chars.html) |
| 4→5 | [The `file` command](https://en.wikipedia.org/wiki/File_%28command%29) |
| 10→11 | [Base64](https://en.wikipedia.org/wiki/Base64) |
| 11→12 | [ROT13](https://en.wikipedia.org/wiki/ROT13) |
| 12→13 | [Hex dump](https://en.wikipedia.org/wiki/Hex_dump) |
| 13→14 | [SSH/OpenSSH/Keys](https://help.ubuntu.com/community/SSH/OpenSSH/Keys) |
| 15→16 | [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) |
| 16→17 | [Port scanner](https://en.wikipedia.org/wiki/Port_scanner) |
| 19→20 | [Setuid](https://en.wikipedia.org/wiki/Setuid) |
| 27→28 through 31→32 | [Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Git from the Bottom Up](https://jwiegley.github.io/git-from-the-bottom-up/) |

### Krypton

| Level | Link |
|---|---|
| 1→2 | [ROT13](https://en.wikipedia.org/wiki/ROT13) |
| 2→3 | [Known-plaintext attack](https://en.wikipedia.org/wiki/Known-plaintext_attack), [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher) |
| 3→4 | [Frequency analysis](https://en.wikipedia.org/wiki/Frequency_analysis) |
| 4→5 | [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher) |
| 5→6 | [Kasiski examination](https://en.wikipedia.org/wiki/Kasiski_examination) |
| 6→7 | [Stream cipher](https://en.wikipedia.org/wiki/Stream_cipher) |

### Natas

| Level | Link |
|---|---|
| 3→4 | [Robots exclusion standard](https://en.wikipedia.org/wiki/Robots.txt) |
| 7→8 | [File inclusion vulnerability](https://en.wikipedia.org/wiki/File_inclusion_vulnerability) |
| 11→12 | [XOR cipher](https://en.wikipedia.org/wiki/XOR_cipher) |
| 14→15 | [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) |

## Keeping this current

The domain list above is generated from each build script's
`EXTRA_INFO` dict. To re-audit after a content change, run from the repo
root:

```bash
grep -ohE 'https?://[a-zA-Z0-9.-]+' scripts/build_bandit.py scripts/build_krypton.py scripts/build_natas.py \
  | sed -E 's#https?://##' | sort -u
```

If that produces a domain not already in the table above, add it here
**and** flag it to whoever maintains `cei-labs-net`'s
`Wargame_Reference_Sites` alias — this doc is the source of truth, that
alias is its network-side mirror, and the two must stay in sync whenever
a new level's hint or "Helpful reading" section links somewhere new.
