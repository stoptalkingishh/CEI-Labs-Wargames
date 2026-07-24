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
priced and debited entirely by the hint-wallet plugin. The three numbers
below are `tier_costs(value)` from `scripts/hint_economy.py` — the *only*
cost formula the wallet ever enforces — not the per-hint text authored in
each `build_<track>.py`'s `HINTS` dict, since that text carries no cost of
its own.

## Fields not in `challenge.yml`, so not fabricated here

- **Estimated duration per level** — not tracked anywhere in this repo.
  Genuinely open; needs real playtester timing data (tracker §3's own P0
  item calls for testing "with representative novice, intermediate, and
  advanced testers," which hasn't happened yet).
- **Owner** — every level is currently unowned (`TBD` across the whole
  tracker). Not invented here.
- **Prerequisites** — CTFd has no configured prerequisite/requirement
  chain for any of these 59 challenges (checked directly). The content
  design assumes sequential play within a track (each level's solution is
  the next level's login), but nothing technically gates level N+1 behind
  level N — a player can jump to any unlocked level. Audience is the same
  across all three tracks: any registered participant/team.

## A real finding surfaced while building this table

**Four levels use a static, non-per-team flag, not the per-team dynamic
flags the rest of the catalog uses**, despite `docs/security-audit-status.md`
describing the static-flags fix as "all 4 phases complete":

| Level | Points | Flag | Why |
| :--- | ---: | :--- | :--- |
| `bandit-start-here` | 10 | `WELCOME_TO_BANDIT` | Onboarding tutorial ("prove you used the launch controls") — no scored content |
| `krypton-start-here` | 10 | `WELCOME_TO_KRYPTON` | Same |
| `natas-start-here` | 10 | `WELCOME_TO_NATAS` | Same |
| `krypton-00` | 200 | `KRYPTONISGREAT` | **Not a tutorial — a real, scored, 200-point challenge.** Has no `instance_type`/target image at all: the ciphertext is embedded directly in the challenge description text (Base64 of a fixed string), so there's no per-team infrastructure to scope a dynamic flag to. Confirmed intentional — `docs/self-hosted-wargames-status.md` explicitly notes "level 0 needs no instance at all." |

The three 10-point tutorials are low-stakes by design and a static flag
there is defensible. `krypton-00` is different: it's real scored content
(200 points, same as `bandit-02`/`natas-00`) with an identical flag for
every team, which is the exact collusion/leakage risk the other 55 levels'
dynamic-flag work was built to close — it's just structurally exempt
because the challenge has no live per-team system to derive a flag from.
That's a legitimate design constraint, not an oversight, but it was never
written down as a deliberate exception anywhere before this table. Worth
either an explicit accepted-risk note (recommended — this is genuinely
fine given the mechanic) or reworking `krypton-00` to embed a per-team
value in its description text (e.g. templated Base64 unique per team),
if full flag-uniqueness coverage is wanted for all 59 levels rather than 58.

### bandit (35 levels)

| ID | Points | Flag source | Instance type | Reset/teardown | Hints (cost) | Expected solve path |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| `bandit-00` | 100 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (10/20/30) | Connect to the server and retrieve the flag. |
| `bandit-01` | 150 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (15/30/45) | Read a file whose name looks like a command-line flag. |
| `bandit-02` | 200 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (20/40/60) | Read a file whose name contains spaces. |
| `bandit-03` | 250 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (25/50/75) | Find a hidden (dotfile) password. |
| `bandit-04` | 300 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (30/60/90) | Find the password among several files in the `inhere` directory. |
| `bandit-05` | 350 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (35/70/105) | Find one specific file among many nested decoys. |
| `bandit-06` | 400 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (40/80/120) | Search the whole filesystem by owner, group, and size. |
| `bandit-07` | 450 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (45/90/135) | Extract a value next to a known marker word. |
| `bandit-08` | 500 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (50/100/150) | Find the one line that appears only once in a large file. |
| `bandit-09` | 550 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (55/110/165) | Pull the readable text out of a mostly-binary file. |
| `bandit-10` | 600 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (60/120/180) | Decode a base64-encoded password. |
| `bandit-11` | 650 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (65/130/195) | Reverse a ROT13 substitution. |
| `bandit-12` | 700 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (70/140/210) | Unwrap several layers of hexdump and compression. |
| `bandit-13` | 750 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (75/150/225) | Use a provided private key to log in as another account. |
| `bandit-14` | 800 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (80/160/240) | Submit a password to a listening TCP service. |
| `bandit-15` | 850 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (85/170/255) | Submit a password over a TLS-encrypted connection. |
| `bandit-16` | 900 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (90/180/270) | Find the one correct service among a range of listening ports. |
| `bandit-17` | 950 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (95/190/285) | Diff two large, nearly-identical files. |
| `bandit-18` | 1000 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (100/200/300) | Read a file without getting an interactive shell. |
| `bandit-19` | 1050 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (105/210/315) | Use a setuid binary to read a file you otherwise couldn't. |
| `bandit-20` | 1100 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (110/220/330) | Have a setuid binary connect back to a listener you control. |
| `bandit-21` | 1150 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (115/230/345) | Read what a cron job does and follow it to the password. |
| `bandit-22` | 1200 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (120/240/360) | Trace a cron job to the script it actually runs. |
| `bandit-23` | 1250 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (125/250/375) | Write your own script for a cron job to run on your behalf. |
| `bandit-24` | 1300 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (130/260/390) | Brute-force a 4-digit PIN against a listening daemon. |
| `bandit-25` | 1350 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (135/270/405) | Escape a restricted, non-bash login shell. |
| `bandit-26` | 1400 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (140/280/420) | Break out of a terminal pager into a shell. |
| `bandit-27` | 1450 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (145/290/435) | Clone a git repository and find a password committed to it. |
| `bandit-28` | 1500 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (150/300/450) | Find a secret that was committed and later removed. |
| `bandit-29` | 1550 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (155/310/465) | Find a secret that only exists on a non-default branch. |
| `bandit-30` | 1600 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (160/320/480) | Find a secret attached to a git tag. |
| `bandit-31` | 1650 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (165/330/495) | Satisfy a repository's own stated requirements to earn the next password. |
| `bandit-32` | 1700 | `per_team_dynamic_fixed` | `single-target` | idle-timeout | 3 (170/340/510) | Reach a real shell from one that mangles every command you type. |
| `bandit-33` | 1750 | `per_team_dynamic_fixed` | `single-target` | **auto on solve** | 3 (175/350/525) | One last escape to finish the track. |
| `bandit-start-here` | 10 | `WELCOME_TO_BANDIT` (static — see finding above) | `single-target` | idle-timeout | 0 | Learn the launch controls, then prove you used them. |

Dependencies: `targets/bandit/` image, `instance_group: bandit`, all
`single-target` (one persistent SSH box per team). Reset method for every
non-auto row above is idle-timeout teardown (`ORCHESTRATOR_IDLE_GRACE_MINUTES`,
default 120 min), not a manual reset button.

### krypton (8 levels)

| ID | Points | Flag source | Instance type | Reset/teardown | Hints (cost) | Expected solve path |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| `krypton-00` | 200 | `KRYPTONISGREAT` (static — see finding above) | **none — no instance, self-contained puzzle** | n/a | 3 (20/40/60) | Decode a Base64-encoded password given directly in the description. |
| `krypton-01` | 250 | `per_team_dynamic_alpha` | `single-target` | idle-timeout | 3 (25/50/75) | Reverse a ROT13 rotation cipher. |
| `krypton-02` | 300 | `per_team_dynamic` | `single-target` | idle-timeout | 3 (30/60/90) | Decrypt a Caesar cipher of unknown shift. |
| `krypton-03` | 350 | `per_team_dynamic_alpha` | `single-target` | idle-timeout | 3 (35/70/105) | Break a substitution cipher using letter-frequency analysis. |
| `krypton-04` | 400 | `per_team_dynamic_alpha` | `single-target` | idle-timeout | 3 (40/80/120) | Break a Vigenère cipher when the key length is already known. |
| `krypton-05` | 450 | `per_team_dynamic_alpha` | `single-target` | idle-timeout | 3 (45/90/135) | Break a Vigenère cipher when the key length isn't given. |
| `krypton-06` | 500 | `per_team_dynamic` | `single-target` | **auto on solve** | 3 (50/100/150) | Recover a repeating keystream and use it to decrypt the final password. |
| `krypton-start-here` | 10 | `WELCOME_TO_KRYPTON` (static — see finding above) | `single-target` | idle-timeout | 0 | Learn the launch controls, then prove you used them. |

Dependencies: `targets/krypton/` image (all levels except `krypton-00`,
which needs no target at all), `instance_group: krypton`.

### natas (16 levels)

| ID | Points | Flag source | Instance type | Reset/teardown | Hints (cost) | Expected solve path |
| :--- | ---: | :--- | :--- | :--- | :--- | :--- |
| `natas-00` | 200 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (20/40/60) | Retrieve the password for the next level from the page source. |
| `natas-01` | 250 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (25/50/75) | Find the password on a page that blocks right-clicking. |
| `natas-02` | 300 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (30/60/90) | Find a password file the page never links to. |
| `natas-03` | 350 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (35/70/105) | Find a path deliberately hidden from search engines. |
| `natas-04` | 400 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (40/80/120) | Forge an HTTP header to satisfy an access check. |
| `natas-05` | 450 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (45/90/135) | Edit a session cookie to change your authorization state. |
| `natas-06` | 500 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (50/100/150) | Read server-side source to find where a secret is stored, then fetch it directly. |
| `natas-07` | 550 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (55/110/165) | Exploit a Local File Inclusion (LFI) vulnerability to read a file the app was never meant to expose. |
| `natas-08` | 600 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (60/120/180) | Reverse a server-side encoding chain to recover a secret. |
| `natas-09` | 650 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (65/130/195) | Inject a shell command through an unsanitized input field. |
| `natas-10` | 700 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (70/140/210) | Achieve the same result once the easy metacharacters are filtered. |
| `natas-11` | 750 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (75/150/225) | Recover an XOR key and forge encrypted data with it. |
| `natas-12` | 800 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (80/160/240) | Upload and execute a web shell. |
| `natas-13` | 850 | `per_team_dynamic` | `target-attacker` | idle-timeout | 3 (85/170/255) | Get a PHP payload past a file-type check based on content, not extension. |
| `natas-14` | 900 | `per_team_dynamic` | `target-attacker` | **auto on solve** | 3 (90/180/270) | Bypass a login form using SQL injection. |
| `natas-start-here` | 10 | `WELCOME_TO_NATAS` (static — see finding above) | `target-attacker` | idle-timeout | 0 | Learn the launch controls, then prove you used them. |

Dependencies: `targets/natas/` (LAMP target) + kali-novnc attacker image,
`instance_group: natas`, `target-attacker` (one target+attacker range per
team — the isolation model documented in `cei-labs-event/docs/
threat-model.md`).

## Totals

35 + 8 + 16 = **59 levels**, matching `game-stages.yml`'s
`expected_challenge_count` for all three staggered-game stages. Points run
sequentially within each track (Bandit 100→1750, Krypton 200/250...500,
Natas 200→900), all `start-here` levels fixed at 10 points.
