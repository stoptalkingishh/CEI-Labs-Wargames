# Challenge inventory

Answers `cei-labs-event/TRACKER.md` §3's P0 item: "Produce a challenge
inventory for all three tracks with ID, audience, objective, prerequisites,
points, flag source, expected solve path, estimated duration, hints, reset
method, dependencies, and owner." Generated directly from each level's
`challenges/<id>/challenge.yml` (the actual CTFd-imported source of truth),
not hand-transcribed — regenerate by re-running the extraction against
current `challenge.yml` files if content changes. Full narrative
walkthroughs already exist per track in `docs/{bandit,krypton,natas}/
writeups.md` and `docs/{bandit,krypton,natas}/cheatsheet.md`; this table
doesn't duplicate that content, it indexes it.

**Hints (cost) is the one column not sourced from `challenge.yml`** — native
CTFd hints (and their point cost) are deliberately absent from that file
(see `scripts/build_bandit.py`'s comment on why); hint credits are instead
priced and debited entirely by the hint-wallet plugin. The cell
`3 (20%/50%/85%)` below is `tier_costs(value)` from
`scripts/hint_economy.py` — the *only* cost formula the wallet ever
enforces — not the per-hint text authored in each `build_<track>.py`'s
`HINTS` dict, since that text carries no cost of its own. Each tier's cost
is a cumulative percentage of the challenge's own point value, applied as a
score reduction at solve time: opening tier 1/2/3 means the solve keeps
80%/50%/15% of the value (tiers are cumulative, not additive — opening all
three costs 85%, not 20+50+85).

## Fields not in `challenge.yml`, so not fabricated here

- **Estimated duration per level** — not tracked anywhere in this repo.
  Genuinely open; needs real playtester timing data (tracker §3's own P0
  item calls for testing "with representative novice, intermediate, and
  advanced testers," which hasn't happened yet).
- **Owner** — every level is currently unowned (`TBD` across the whole
  tracker). Not invented here.
- **Prerequisites** — CTFd has no configured prerequisite/requirement
  chain for any of these 65 challenges (checked directly). The content
  design assumes sequential play within a track (each level's solution is
  the next level's login), but nothing technically gates level N+1 behind
  level N — a player can jump to any unlocked level. Audience is the same
  across all three tracks: any registered participant/team.

## A real finding surfaced while building this table

**Three levels use a static, non-per-team flag, not the per-team dynamic
flags the rest of the catalog uses.** (Originally four — `krypton-00` was
the fourth; see "Resolved" below.)

| Level | Points | Flag | Why |
| :--- | ---: | :--- | :--- |
| `bandit-start-here` | 10 | `Do not use AI or external tools/services to cheat or obtain answers.` | Onboarding tutorial ("prove you used the launch controls") — no scored content |
| `krypton-start-here` | 10 | `Do not use AI or external tools/services to cheat or obtain answers.` | Same |
| `natas-start-here` | 10 | `WELCOME TO NATAS` | Same |

The three 10-point tutorials are low-stakes by design and a static flag
there is defensible.

**Resolved (cei-labs-event#17):** `krypton-00` used to be the exception
to that "low-stakes only" rule — a real, scored, 200-point challenge
(same as `bandit-02`/`natas-00`) with an identical flag for every team,
the exact collusion/leakage risk the other levels' dynamic-flag work was
built to close, because it had no live per-team system to derive a flag
from (no `instance_type`, no target account — the ciphertext was a fixed
Base64 string embedded directly in the description text). It now has a
real `krypton0` account on the same shared Krypton box as levels 1-6,
with a per-team Base64 secret written into its home directory by
`entrypoint.sh` at container start — the same per-team-dynamic mechanism
every other level uses. All 59 *staged* challenges now have per-team-unique
flags; the 6 unstaged AI Copilot Setup challenges (below) are static by
design — they prove local setup work, not shared-box solves.

### bandit (35 levels)

| ID | Points | Flag source | Instance type | Reset/teardown | Hints (cost) | Expected solve path |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| `bandit-00` | 100 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Connect to the server and retrieve the flag. |
| `bandit-01` | 150 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Read a file whose name looks like a command-line flag. |
| `bandit-02` | 200 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Read a file whose name contains spaces. |
| `bandit-03` | 250 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Find a hidden (dotfile) password. |
| `bandit-04` | 300 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Find the password among several files in the `inhere` directory. |
| `bandit-05` | 350 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Find one specific file among many nested decoys. |
| `bandit-06` | 400 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Search the whole filesystem by owner, group, and size. |
| `bandit-07` | 450 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Extract a value next to a known marker word. |
| `bandit-08` | 500 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Find the one line that appears only once in a large file. |
| `bandit-09` | 550 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Pull the readable text out of a mostly-binary file. |
| `bandit-10` | 600 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Decode a base64-encoded password. |
| `bandit-11` | 650 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Reverse a ROT13 substitution. |
| `bandit-12` | 700 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Unwrap several layers of hexdump and compression. |
| `bandit-13` | 750 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Use a provided private key to log in as another account. |
| `bandit-14` | 800 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Submit a password to a listening TCP service. |
| `bandit-15` | 850 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Submit a password over a TLS-encrypted connection. |
| `bandit-16` | 900 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Find the one correct service among a range of listening ports. |
| `bandit-17` | 950 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Diff two large, nearly-identical files. |
| `bandit-18` | 1000 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Read a file without getting an interactive shell. |
| `bandit-19` | 1050 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Use a setuid binary to read a file you otherwise couldn't. |
| `bandit-20` | 1100 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Have a setuid binary connect back to a listener you control. |
| `bandit-21` | 1150 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Read what a cron job does and follow it to the password. |
| `bandit-22` | 1200 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Trace a cron job to the script it actually runs. |
| `bandit-23` | 1250 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Write your own script for a cron job to run on your behalf. |
| `bandit-24` | 1300 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Brute-force a 4-digit PIN against a listening daemon. |
| `bandit-25` | 1350 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Escape a restricted, non-bash login shell. |
| `bandit-26` | 1400 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Break out of a terminal pager into a shell. |
| `bandit-27` | 1450 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Clone a git repository and find a password committed to it. |
| `bandit-28` | 1500 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Find a secret that was committed and later removed. |
| `bandit-29` | 1550 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Find a secret that only exists on a non-default branch. |
| `bandit-30` | 1600 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Find a secret attached to a git tag. |
| `bandit-31` | 1650 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Satisfy a repository's own stated requirements to earn the next password. |
| `bandit-32` | 1700 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Reach a real shell from one that mangles every command you type. |
| `bandit-33` | 1750 | `per_team_dynamic_fixed` | `single-target` | **auto on solve** | 3 (20%/50%/85%) | One last escape to finish the track. |
| `bandit-start-here` | 10 | `Do not use AI or external tools/services to cheat or obtain answers.` (static — see finding above) | `single-target` | idle-timeout | 0 | Learn the launch controls, then prove you used them. |

Dependencies: `targets/bandit/` image, `instance_group: bandit`, all
`single-target` (one persistent SSH box per team). Reset method for every
non-auto row above is idle-timeout teardown (`ORCHESTRATOR_IDLE_GRACE_MINUTES`,
default 120 min), not a manual reset button.

### krypton (8 levels)

| ID | Points | Flag source | Instance type | Reset/teardown | Hints (cost) | Expected solve path |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| `krypton-00` | 200 | `per_team_dynamic` (fixed no longer — see cei-labs-event#17) | `single-target` | idle-timeout | 3 (20%/50%/85%) | Log in as `krypton0` (fixed public password `krypton0`) and decode a per-team Base64-encoded string in the home directory. |
| `krypton-01` | 250 | `per_team_dynamic_alpha` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Reverse a ROT13 rotation cipher. |
| `krypton-02` | 300 | `per_team_dynamic` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Decrypt a Caesar cipher of unknown shift. |
| `krypton-03` | 350 | `per_team_dynamic_alpha` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Break a substitution cipher using letter-frequency analysis. |
| `krypton-04` | 400 | `per_team_dynamic_alpha` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Break a Vigenère cipher when the key length is already known. |
| `krypton-05` | 450 | `per_team_dynamic_alpha` | `single-target` | idle-timeout | 3 (20%/50%/85%) | Break a Vigenère cipher when the key length isn't given. |
| `krypton-06` | 500 | `per_team_dynamic` | `single-target` | **auto on solve** | 3 (20%/50%/85%) | Recover a repeating keystream and use it to decrypt the final password. |
| `krypton-start-here` | 10 | `Do not use AI or external tools/services to cheat or obtain answers.` (static — see finding above) | `single-target` | idle-timeout | 0 | Learn the launch controls, then prove you used them. |

Dependencies: `targets/krypton/` image (all 8 levels including
`krypton-00`, which now has its own `krypton0` account like every other
level), `instance_group: krypton`.

### natas (36 levels)

| ID | Points | Flag source | Instance type | Reset/teardown | Hints (cost) | Expected solve path |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| `natas-00` | 200 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Retrieve the password for the next level from the page source. |
| `natas-01` | 250 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Find the password on a page that blocks right-clicking. |
| `natas-02` | 300 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Find a password file the page never links to. |
| `natas-03` | 350 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Find a path deliberately hidden from search engines. |
| `natas-04` | 400 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Forge an HTTP header to satisfy an access check. |
| `natas-05` | 450 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Edit a session cookie to change your authorization state. |
| `natas-06` | 500 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Read server-side source to find where a secret is stored, then fetch it directly. |
| `natas-07` | 550 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Exploit a Local File Inclusion (LFI) vulnerability to read a file the app was never meant to expose. |
| `natas-08` | 600 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Reverse a server-side encoding chain to recover a secret. |
| `natas-09` | 650 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Inject a shell command through an unsanitized input field. |
| `natas-10` | 700 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Achieve the same result once the easy metacharacters are filtered. |
| `natas-11` | 750 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Recover an XOR key and forge encrypted data with it. |
| `natas-12` | 800 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Upload and execute a web shell. |
| `natas-13` | 850 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Get a PHP payload past a file-type check based on content, not extension. |
| `natas-14` | 900 | `per_team_dynamic` | `target-attacker` | **auto on solve** | 3 (20%/50%/85%) | Bypass a login form using SQL injection. |
| `natas-15` | 950 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Query a bounded boolean response oracle. |
| `natas-16` | 1000 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Search controlled in-memory training data. |
| `natas-17` | 1050 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Compare deterministic response timing. |
| `natas-18` | 1100 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Inspect bounded numeric session state. |
| `natas-19` | 1150 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Decode a bounded session token. |
| `natas-20` | 1200 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Trace a controlled session record. |
| `natas-21` | 1250 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Compare two internal session scopes. |
| `natas-22` | 1300 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Inspect redirect and response behavior. |
| `natas-23` | 1350 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Contrast toy numeric and strict comparisons. |
| `natas-24` | 1400 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Validate a bounded alternate request shape. |
| `natas-25` | 1450 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Trace a synthetic audit resolver. |
| `natas-26` | 1500 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Validate a JSON virtual export. |
| `natas-27` | 1550 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Inspect an identity normalization model. |
| `natas-28` | 1600 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Reason about a visual block token model. |
| `natas-29` | 1650 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Use a virtual command catalog. |
| `natas-30` | 1700 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Trace repeated parameters through a mock query model. |
| `natas-31` | 1750 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Select an allowlisted virtual artifact. |
| `natas-32` | 1800 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Use a fixed command emulator. |
| `natas-33` | 1850 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20%/50%/85%) | Record inert upload metadata. |
| `natas-34` | 1900 | `per_team_dynamic` | `target-attacker` | **auto on solve** | 3 (20%/50%/85%) | Complete the terminal debrief. |
| `natas-start-here` | 10 | `WELCOME TO NATAS` (static — see finding above) | `target-attacker` | idle-timeout | 0 | Learn the launch controls, then prove you used them. |

Dependencies: `targets/natas/` (LAMP target) + kali-novnc attacker image,
`instance_group: natas`, `target-attacker` (one target+attacker range per
team — the isolation model documented in `cei-labs-event/docs/
threat-model.md`).

### AI Copilot Setup (6 challenges)

This track has no per-team Docker instance at all — the "target" is the
player's own laptop (see `scripts/build_agent.py`'s header). Flags are
static, but each is only learnable by running `ctf-agent-verify` locally
and passing the real milestone, so a static flag here does not carry the
collusion risk discussed above: the *work*, not the string, is the proof.
Hidden by default (`RELEASE_STATE` in `scripts/build_agent.py`) — the
organizer releases it manually.

| ID | Points | Flag source | Instance type | Reset/teardown | Hints (cost) | Expected solve path |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| `cei-agent-start-here` | 10 | static (orientation) | none (player's laptop) | n/a | 0 | Read the track intro and confirm the setup goal. |
| `cei-agent-01-ollama` | 100 | static via `ctf-agent-verify` | none | n/a | 0 | Install Ollama and get it running. |
| `cei-agent-02-model` | 100 | static via `ctf-agent-verify` | none | n/a | 0 | Pull at least one model. |
| `cei-agent-03-install` | 100 | static via `ctf-agent-verify` | none | n/a | 0 | Install the `ctf-agent` package and launch it. |
| `cei-agent-04-ssh` | 150 | static via `ctf-agent-verify` | none | n/a | 0 | Point the agent at a challenge box and complete a live SSH round-trip. |
| `cei-agent-05-prompt` | 150 | static via `ctf-agent-verify` | none | n/a | 0 | Ask for help using the documented prompt shape. |

## Totals

35 + 8 + 36 = **79 staged levels**, matching `game-stages.yml`'s
`expected_challenge_count` for all three staggered-game stages, plus the
6 deliberately-unstaged AI Copilot Setup challenges above = **85
challenges total** (the same split `scripts/validate_generated.py`
encodes as `UNSTAGED_TRACK_CHALLENGE_COUNT`). Points run
sequentially within each track (Bandit 100→1750, Krypton 200/250...500,
Natas 200→1900), all `start-here` levels fixed at 10 points.
