# Self-Hosted Wargames Blueprint: Bandit, Krypton, Natas

**Status:** Planning document, being committed to a working branch now to
preserve state before implementation starts.
**Owner repos touched:** `CEI-Labs-Wargames` (primary), `cei-labs-engine`
(one Dockerfile change — see Decision 2, now resolved), `cei-labs-net`
(docs only, likely no changes).

## Why this exists

`CEI-Labs-Wargames` currently generates CTFd challenges whose descriptions
point players at OverTheWire's real public infrastructure
(`bandit.labs.overthewire.org`, `natasN.natas.labs.overthewire.org`) with
**hardcoded flags baked in at content-generation time**. This breaks in two
ways: OTW periodically resets/rebuilds those public boxes (rotating
per-level credentials), and OTW's real design requires *discovering* each
next password by exploiting the current level — a hardcoded flag list
can't reflect that if the upstream state ever drifts. The fix is to
self-host equivalent environments we fully control.

## Confirmed facts this plan is built on (do not re-derive, re-verify only if something looks off)

**Real game mechanics** (verified via OverTheWire's site + community
write-ups, current as of 2026-07):

| Game | Access | Levels (OTW upstream) | Levels (already authored in `CEI-Labs-Wargames`) | Topic |
| :--- | :--- | :--- | :--- | :--- |
| Bandit | SSH, `bandit.labs.overthewire.org:2220` | 34 (0–33) | **34** — full parity | Linux fundamentals: permissions, `find`/`grep`, setuid, cron, git, ssh keys |
| Krypton | SSH, `krypton.labs.overthewire.org:2231` (different port than Bandit) | ~8 (0–7) | **7** — full parity | Base64, ROT13, Caesar, Vigenère (known-length), Vigenère (Kasiski), stream cipher/LFSR |
| Natas | HTTP Basic Auth, `natasN.natas.labs.overthewire.org`, one PHP app per level | 34+ (0–33+) | **15** — curated subset | Auth bypass, SQLi, LFI, command injection, weak crypto, file upload, cookie forgery, PHP object injection |

**This is a scoped job**: self-host what's already authored (34 + 7 + 15 =
56 challenges, already live in CTFd per earlier testing), not expand to
OTW's full upstream catalog. Both Bandit and Krypton are, in reality,
**one single shared machine per player** that you progress through by
escalating to the next level's user — not 34 (or 7) separate machines.
Natas is, in reality, **one single web server** hosting many vhosts, with
per-level Unix users controlling which password files are readable from
which level.

### Natas's real stack — researched and confirmed

Community write-ups consistently confirm: **PHP + Apache + MySQL (a LAMP
stack)**, exactly as expected. PHP source visible in leaked/quoted level
code calls `mysql_connect('localhost', 'natasN', '<password>')` for
SQL-backed levels, and every level's next-level password lives in
`/etc/natas_webpass/natasN`, permissioned so only Unix users `natas(N-1)`
and `natasN` can read it.

**The one thing not publicly documented is *how* OTW gets each vhost's PHP
to execute as that level's distinct Unix user** (standard Apache+mod_php
runs everything as one shared `www-data` — that alone would not produce
the per-level file permission boundary Natas depends on). No official
infrastructure write-up describes their exact mechanism. Rather than
guess at OTW's undocumented internals, this plan uses a **modern, still-
maintained, well-documented equivalent that produces the identical
externally-observable behavior**:

- **Apache MPM-ITK** (`libapache2-mpm-itk`) — confirmed packaged and
  installable on Debian 12 "bookworm" (the same base this project already
  standardizes on for `operator/targets/base-linux`). Its `AssignUserID
  <user> <group>` directive, set inside each `<VirtualHost>` block, makes
  that entire vhost — including all PHP execution under it — run as the
  specified Unix user/group. One Apache install, one config file, 15
  vhosts, 15 `AssignUserID` lines: `natas0`'s PHP genuinely runs as
  `natas0`, `natas1`'s genuinely runs as `natas1`, etc. This reproduces
  the real password-file permission boundary exactly, not just in
  appearance.
- **Fallback if MPM-ITK proves incompatible during build** (e.g. an
  unexpected conflict with the Debian slim base, or the module is
  dropped from the repo before implementation): PHP-FPM with **one pool
  per level**, each pool's `user`/`group` directive set to that level's
  account, and Apache (`mod_proxy_fcgi`) or nginx routing each vhost to
  its own pool by socket path. Functionally equivalent; more moving parts
  (N pool configs instead of N `AssignUserID` lines), so MPM-ITK is the
  primary plan and this is documented now so a fallback decision doesn't
  block the whole phase if hit.
- **Database**: MariaDB, not MySQL — matches what `cei-labs-engine`
  already runs for CTFd's own DB (`mariadb:10.11`), keeping one DB engine
  across the whole platform rather than introducing a second. MariaDB is
  a drop-in-compatible fork; nothing in a "MySQL" write-up implies
  anything MariaDB can't do.

**`cei-labs-engine` already provides the infrastructure primitives this
needs** — confirmed by reading the actual source, not assumed:

- `operator/targets/base-linux/Dockerfile` — a minimal `debian:12-slim` +
  `openssh-server` image, explicitly documented as "FROM'd by specific
  challenge images in the wargames repo." **This is already the exact
  hybrid base image the design calls for.** No new generic base image
  needs to be built for Bandit/Krypton.
- `operator/kali-novnc/Dockerfile` — a full Kali-rolling + xfce4 + noVNC
  attacker workstation, already wired as the example `attacker_image` in
  the orchestrator's own README. Has nmap/gobuster/sqlmap/john/hashcat/
  python3/curl/wget/git/tmux/vim etc. already installed. **Has no SSH
  server today** — noVNC (port 6080) is its only access path.
- `docker/orchestrator/app/instance_types.py` — three instance types:
  - `single-target`: one container, its own airgapped network, one
    directly-published port (SSH by default, per `docker/.env.example`'s
    `30000-32767` range). **This is Bandit and Krypton, exactly as-is.**
  - `target-attacker`: one shared, Traefik-routed attacker (noVNC) per
    *team*, plus any number of targets on a private range network
    reachable only from that team's own attacker. **This is Natas,
    exactly as-is** — target = the vulnerable LAMP web app, attacker =
    the Kali box.
  - `web-app`: Traefik-routed, single container (used for Juice Shop) —
    not relevant here.
- `docker/ctfd/plugins/instance-launcher/models.py` — `InstanceChallengeConfig.instance_group`:
  **"Multiple challenges can share one deployment... by setting the SAME
  instance_group... whichever challenge in the group is launched first is
  what actually creates the container."** This is precisely "many levels,
  one persistent machine" — already built, zero new orchestration code
  needed. `shutdown_on_solve` + group-aware countdown ("only starts once
  EVERY challenge in the group... has been solved") already implements
  "persistent until it needs to be shut down."
- Challenge YAML already supports declaring `instance_type`, `image`/
  `port` (single-target), or `target_image`/`attacker_image`/
  `attacker_port` (target-attacker) directly — see
  `challenges/sprint2-web/challenges.yml`'s Juice Shop entries for the
  working pattern. `scripts/challenges-load.sh` has an "instance-mapping
  sync step" that reads these into `InstanceChallengeConfig` rows.

**Conclusion**: this blueprint is *not* "build new orchestration." It's
"build the actual Bandit/Krypton/Natas container images and wire their
challenge YAML to the instance types that already exist."

## Decisions — now resolved

1. **Natas attacker access model — RESOLVED: keep both.** Confirmed: the
   noVNC Kali station should support **multiple ways of interacting**
   (browser/GUI via noVNC, and SSH for players who are more comfortable
   at a terminal) — this is deliberate, not a compromise. Both access
   paths stay: noVNC on 6080 (Traefik-routed, exactly as the orchestrator
   already supports) **and** SSH on 22 (directly on the same container).
2. **New image or extend the existing one — RESOLVED: extend the existing
   `operator/kali-novnc` image.** Add `openssh-server` + a matching
   `useradd`/`chpasswd`/`ENABLE ssh` block to the same Dockerfile that
   already builds the `operator` user for VNC — same account, same
   password, logs in identically whether over noVNC or SSH. No second,
   parallel image to maintain. The existing forensics/analyst tooling
   (Wireshark, Ghidra, sleuthkit, etc.) stays — it's not in the way of
   web-exploitation work, and this image already serves the broader
   analyst/SOC roadmap beyond just Natas, so it isn't being trimmed down
   for one use case.
3. **Base OS for the Bandit/Krypton/Natas target images — CONFIRMED:**
   `operator/targets/base-linux` (`debian:12-slim`), extended per-target.
   Natas additionally needs Apache/MariaDB/PHP/MPM-ITK layered on top —
   still Debian 12, still one base-image family project-wide.

## Phase 1 — Base Image Work (cei-labs-engine)

- [ ] **`operator/kali-novnc/Dockerfile`**: add `openssh-server` to the
      `apt-get install` list; add `mkdir -p /var/run/sshd`; generate a
      host key at build time (`ssh-keygen -A`); ensure the existing
      `operator` user's password (already set from `VNC_PASSWORD`) works
      for SSH login too (no separate credential to manage — same
      variable, same value, both protocols).
  - [ ] **Verify:** `docker build` succeeds; `docker run` the image
        standalone, confirm `sshd` starts (check `docker logs` /
        `ps aux` inside the container) alongside the existing VNC/noVNC
        startup script — the two must not race or fight over the startup
        script's `tail -f /dev/null` foreground-keeper pattern. Update
        `/start.sh` to launch `sshd` explicitly (`/usr/sbin/sshd`
        daemonizes on its own; don't background it manually and lose the
        PID).
  - [ ] **Verify:** `EXPOSE 22` added alongside the existing `EXPOSE
        6080`; confirm both ports are listed in `docker inspect`.
  - [ ] **Verify:** SSH in as `operator` with the same password used for
        VNC, from a separate test container on the same Docker network —
        confirms the credential is genuinely shared, not two separate
        auth paths that happen to coincide today and drift later.
- [ ] Confirm `operator/targets/base-linux` needs **no changes** for
      Bandit/Krypton (already has `openssh-server`, `netcat-openbsd`,
      `curl`, `iproute2`) — this is a check, not an implementation step;
      only act if something's actually missing once Phase 2 starts.
- [ ] **Read, don't guess:** open `scripts/challenges-load.sh` in full
      and confirm the exact YAML key names its "instance-mapping sync
      step" reads (`instance_type`, `image`, `target_image`,
      `attacker_image`, `attacker_port`, and — needs confirming —
      `instance_group`, `shutdown_on_solve`). Record the confirmed field
      names here before writing any Phase 5/Phase 2-4 YAML, since a
      silently-wrong key name would fail invisibly (CTFd would just show
      no "Launch Environment" button, with no obvious error).
  - [ ] **Verify:** cross-check the confirmed field names against
        `docker/ctfd/plugins/instance-launcher/models.py`'s
        `InstanceChallengeConfig` columns (already read — listed above)
        to make sure the sync script's YAML parsing and the DB model
        agree on every field name.

## Phase 2 — Bandit Self-Hosted Target (34 levels, one persistent machine)

- [ ] New repo location: `CEI-Labs-Wargames/targets/bandit/Dockerfile`,
      `FROM` `cei-labs-engine`'s `operator/targets/base-linux` (pin an
      image tag/digest, don't float `:latest`).
- [ ] Recreate the real Bandit filesystem/privilege structure faithfully:
  - [ ] One Unix user per level (`bandit0` through `bandit33`), matching
        real OTW's naming.
    - [ ] **Verify:** `id banditN` for all 34 users succeeds inside a
          built test container; no UID collisions; home directories
          exist at `/home/banditN` with correct ownership.
  - [ ] Level 0's password is a known, fixed value handed out in the
        CTFd challenge description (mirrors OTW's public level-0
        credential).
  - [ ] Each level N's home directory contains whatever artifact teaches
        that level's lesson (hidden files, SUID binaries, cron jobs, git
        repos, compressed/encoded files, etc.) — content-author each of
        the 34 lessons; reuse write-ups only to confirm the *teaching
        mechanism* per level, do not copy OTW's actual passwords/binaries
        verbatim.
    - [ ] **Verify per level, not just at the end:** as each level's
          artifact is authored, immediately `docker exec` in as that
          level's user and confirm the artifact behaves as intended
          (e.g. the SUID binary actually needs elevated privilege to do
          its job; the cron job actually fires on schedule; the hidden
          file is actually hidden but findable via the intended command)
          — catching a broken level during authoring is far cheaper than
          catching it in Phase 7's full playthrough.
  - [ ] Each level N's password file is readable only by user N (and
        possibly N+1, matching OTW's actual permission model) — this is
        the core mechanic, get the permission bits exactly right per
        level.
    - [ ] **Verify:** for every level N, `su banditN -c "cat
          /path/to/passwordfile"` succeeds, and `su bandit(N-2) -c "cat
          /path/to/passwordfile"` (a user two levels back, not the
          intended predecessor) fails with permission denied — confirms
          the boundary is exactly where intended, not accidentally wider.
- [ ] Install the level-specific tools actually required to solve each of
      the 34 lessons (this *is* the multi-version tool requirement for
      Bandit — driven by what the lessons need, not a generic list):
      `find`, `grep`, `awk`, `sed`, `sort`, `diff`, `file`, `strings`,
      `tar`, `gzip`, `bzip2`, `xz`, `git`, `cron`/`at`, `openssh-client`
      (one Bandit level requires SSH-ing to a different local port),
      `nc`/`ncat`/`socat` (install all three — matches "multiple tools
      so users can use what they're comfortable with"), `python3` (and
      `python2` if any lesson expects it), two editors (`vim` + `nano`).
  - [ ] **Verify:** `which <tool>` for every tool on this list succeeds
        inside the built image; no lesson silently depends on a tool that
        didn't make the list (cross-check against the per-level content
        authored above).
- [ ] Read-only root filesystem where the level design allows it; only
      the specific files/dirs a level needs to be writable should be.
  - [ ] **Verify:** with `read_only: true` set at run time, attempt a
        write to a path *not* on the explicit writable allowlist and
        confirm it fails; attempt a write to a path that *is* on the
        allowlist (e.g. wherever a level intentionally needs scratch
        space) and confirm it succeeds.
- [ ] `EXPOSE 22` only. No other ports.
- [ ] `docker-entrypoint`/`CMD`: `sshd -D`, matching the base image's
      existing default.
- [ ] Strip build-time-only packages (compilers, package manager caches)
      in the same `RUN` layer they were installed in — multi-stage build
      if any level needs compiled artifacts.

### Wiring into CTFd (Bandit)

- [ ] Update `scripts/build_bandit.py`: for each of the 34 challenges,
      set `instance_type: single-target`, `image:
      ghcr.io/<org>/cei-labs-wargames/bandit-target:<tag>`,
      `instance_group: bandit` (same group value on all 34), and a
      `shutdown_on_solve` policy — recommend **only the LAST level
      (Bandit 33) sets `shutdown_on_solve: true`**, all earlier levels
      `false`, so the box doesn't tear down mid-progression when a player
      solves an early level slower than a later one, or replays an
      earlier level.
  - [ ] **Verify:** read `solve_hook.py`'s actual group-evaluation logic
        and confirm this "only the last level triggers shutdown" setup
        produces the intended behavior (countdown starts only once *all*
        `shutdown_on_solve: true` challenges in the group are solved —
        with only one such challenge in the group, that's equivalent to
        "starts when Bandit 33 is solved," which is what's wanted; if the
        actual logic differs, adjust the plan here before implementing).
- [ ] Rewrite each level's `description` to drop the OTW hostname/port
      references and instead say something like "Click Launch Environment
      below to get your own private Bandit box" — connection details are
      now dynamic (per-team `single-target` port), not static text.
- [ ] Keep the flags as-is (self-authored, not OTW's) — only the
      environment changes, not the answer-checking mechanism.

## Phase 3 — Krypton Self-Hosted Target (7 levels, one persistent machine)

Same pattern as Phase 2, scaled to Krypton's smaller, crypto-focused scope.
Every "Verify" item from Phase 2 applies here too (per-user isolation
check, per-tool `which` check, read-only-rootfs check) — not repeated
verbatim below to keep this section shorter; treat Phase 2's verification
checklist as the template.

- [ ] `CEI-Labs-Wargames/targets/krypton/Dockerfile`, `FROM` the same
      `operator/targets/base-linux` base.
- [ ] One Unix user per level (`krypton0`–`krypton6`), same
      permission-escalation mechanic as Bandit.
  - [ ] **Verify:** same `id`/`su`-based permission-boundary check as
        Phase 2.
- [ ] Per-level content matching the 7 already-authored topics: Base64,
      ROT13, Caesar, Vigenère (known-length), Vigenère (Kasiski), stream
      cipher/LFSR, plus whichever 7th topic the current `build_krypton.py`
      already defines.
  - [ ] **Verify:** open `scripts/build_krypton.py`'s existing
        `challenges_data` list and confirm this plan's 7-topic list
        matches it exactly (name-for-name) before authoring content —
        do not re-derive the topic list from memory/research a second
        time.
  - [ ] **Verify per level:** as each cipher challenge is authored,
        independently encode/decode it outside the container (a quick
        Python one-liner) to confirm the ciphertext placed on the box
        actually decodes to the expected plaintext/next-password with
        the documented method — a transcription error here silently
        breaks the level.
- [ ] Crypto tooling, with alternatives installed side by side so players
      can use whichever they know: `python3` (`pycryptodome` or similar
      for stream-cipher/LFSR work), `openssl` CLI, `xxd` and `hexdump`
      (both), `base64`/`base32`, `tr` (classic Caesar/ROT13 one-liners).
  - [ ] **Verify:** `which <tool>` check, same as Phase 2.
- [ ] Same hardening/read-only/EXPOSE-22-only rules as Phase 2.

### Wiring into CTFd (Krypton)

- [ ] Update `scripts/build_krypton.py`: `instance_type: single-target`,
      shared `instance_group: krypton`, `shutdown_on_solve: true` only on
      the final level, same pattern as Bandit.
- [ ] Rewrite descriptions to drop the OTW hostname references.

## Phase 4 — Natas Self-Hosted LAMP Target + Kali Attacker (15 levels, one web server + one shared attacker per team)

### 4a. Target image — the LAMP stack itself

- [ ] `CEI-Labs-Wargames/targets/natas/Dockerfile`, `FROM`
      `operator/targets/base-linux` (`debian:12-slim`).
- [ ] Install: `apache2`, `libapache2-mpm-itk`, `php`, `libapache2-mod-php`
      (or the PHP version matching whichever levels need specific PHP
      behavior — confirm PHP major version doesn't affect any of the 15
      authored lessons before pinning one), `mariadb-server` (or
      `mariadb-server` in the same container for simplicity, since this
      is a single-purpose disposable-per-team box, not a shared service —
      no need for a separate DB container here the way `cei-labs-engine`
      does for CTFd's own DB).
  - [ ] **Verify:** `apache2ctl -M` inside the built image lists `mpm_itk`
        as the active MPM (not `prefork`/`event`/`worker` — MPM-ITK
        replaces the MPM entirely, it isn't a bolt-on module; confirm no
        conflicting MPM package got pulled in as a dependency).
- [ ] One Apache `<VirtualHost>` block per level (`natas0`–`natas14`),
      each with its own `AssignUserID natasN natasN` line, its own
      `DocumentRoot`, and — for levels the real game distinguishes by
      port/vhost-name rather than path — matched by whatever the
      already-authored 15 lessons actually expect (confirm the exact
      addressing scheme, e.g. distinct ports vs. `Host:` header vhosts,
      against `build_natas.py`'s current descriptions before finalizing
      the Apache config).
  - [ ] **Verify:** `natas0`'s PHP process genuinely runs as Unix user
        `natas0`, not `www-data` or `root` — from inside the container,
        trigger a request to `natas0`'s vhost and inspect the running
        process owner (`ps aux` filtered to the Apache worker handling
        that request) while the request is in flight, or have the
        vhost's PHP write `getmyuid()`/`posix_getpwuid()` output
        somewhere inspectable for this one verification pass (remove
        before shipping).
  - [ ] **Verify:** repeat for at least 3 more levels spanning the range
        (e.g. natas4, natas9, natas14) — don't assume the first level
        working means `AssignUserID` is correctly set on all 15.
- [ ] One Unix user per level (`natas0`–`natas14`); `/etc/natas_webpass/natasN`
      files with the real permission model: readable only by `natas(N-1)`
      and `natasN`.
  - [ ] **Verify:** `su natasN -c "cat /etc/natas_webpass/natasN"`
        succeeds; `su natas(N-2) -c "cat /etc/natas_webpass/natasN"`
        (two levels back) fails — identical boundary check to
        Bandit/Krypton, applied to the file-based (not shell-based)
        access path Natas actually uses.
- [ ] MariaDB: create the specific databases/tables/users the SQLi-related
      lessons need (matching whatever `build_natas.py`'s existing SQLi
      level descriptions imply about the schema) — content-author this
      alongside the PHP for those specific levels, not generically.
  - [ ] **Verify:** `mysql -u natasN -p<password> -e "SHOW TABLES"` (run
        as that level's intended low-privilege DB user, not root) returns
        exactly the tables that level's lesson expects to be reachable —
        confirms the DB-level privilege boundary matches the file-level
        one.
- [ ] Content-author each of the 15 vulnerability lessons (auth bypass,
      SQLi, LFI, command injection, weak crypto, file upload, cookie
      forgery, PHP object injection — matching whatever `build_natas.py`'s
      existing 15 entries already describe).
  - [ ] **Verify per level as authored:** actually exploit it yourself
        (or delegate a full pass to the Phase 7 playthrough, but at
        minimum smoke-test each as it's written) — confirm the intended
        vulnerability is present, exploitable via the intended technique,
        and yields the next level's access/password through that
        technique specifically, not through some unintended shortcut.
- [ ] Read-only filesystem for anything not intentionally
      vulnerable-and-writable as part of a specific lesson (e.g. a
      file-upload level legitimately needs one writable directory — scope
      that narrowly).
  - [ ] **Verify:** same read-only/writable-allowlist check as Phase 2,
        applied per-vhost since each level may have a different scope of
        legitimate writability.
- [ ] **No externally published port at all** on this container — per
      the `target-attacker` model, it's reachable only from its own
      range's attacker over the private range network. This already
      satisfies "isolated unless the question needs it" and "no inbound
      except SSH" even more strictly (it has *no* inbound from outside
      the range, full stop — not even SSH).
  - [ ] **Verify:** from outside the range network entirely (e.g. from
        the Docker host, or another team's range), confirm the Natas
        target is completely unreachable on any port.

### 4b. Attacker image — extend `kali-novnc` (per resolved Decision 2)

- [ ] Confirm Phase 1's `operator/kali-novnc` SSH addition is complete
      and pushed before using it as `attacker_image` here.
- [ ] Web-exploitation-relevant tools already present in `kali-novnc`
      (confirm via the Dockerfile, don't reinstall): `nmap`, `gobuster`,
      `sqlmap`, `python3`, `curl`, `wget`, `git`, `tmux`, `vim`. Add what's
      missing for web work specifically:
  - [ ] `ffuf` (directory/parameter brute-forcing alternative to
        `gobuster` — "multiple tools so users can feel comfortable")
  - [ ] `mitmproxy` (intercepting proxy — Burp Suite Community isn't
        freely redistributable in a base image; document in the
        challenge-facing README how a player can tunnel their own Burp
        through this box via SSH port-forwarding instead, if they prefer
        it)
  - [ ] `nano` (second editor alongside the existing `vim`)
  - [ ] `netcat-traditional` is already present; add `ncat` and `socat`
        alongside it for the same "pick your favorite" reasoning used on
        the Bandit/Krypton boxes
  - [ ] `python3-requests` explicitly (confirm it's pulled in already via
        some other dependency, or add it directly — most Natas scripting
        write-ups lean on `requests`)
  - [ ] **Verify:** `which <tool>` for the full combined list (existing +
        additions) succeeds in the rebuilt image.
- [ ] Confirm this attacker container, once launched as part of a Natas
      range, can resolve and reach the Natas target's internal hostname
      (`naming.range_target_service_name` — read that function's actual
      output format before writing this check) over HTTP, and cannot
      reach anything else.
  - [ ] **Verify:** from inside the attacker (via SSH or noVNC terminal),
        `curl http://<target-hostname>/` succeeds; `curl` or `nmap` any
        address outside the range network (another team's range, CTFd,
        the orchestrator) fails/times out.

### Wiring into CTFd (Natas)

- [ ] Update `scripts/build_natas.py`: `instance_type: target-attacker`,
      `target_image: .../natas-target:<tag>`, `attacker_image:
      .../ctf-kali-novnc:<tag>` (the extended existing image, per
      resolved Decision 2 — not a new separate image name), shared
      `instance_group: natas` across all 15 challenges.
- [ ] Rewrite descriptions to reference "Launch Environment" instead of
      OTW hostnames; mention that both noVNC (browser) and SSH access are
      available, so players pick whichever they're comfortable with.

## Phase 5 — Cross-Repo Consistency Check

- [ ] Confirm no `cei-labs-net` changes are actually needed:
      `single-target` and `target-attacker` both already fall within the
      documented `10.10.20.0/24:30000-32767` (SSH/target ports) and
      `:80,443` (Traefik/noVNC) rules from the earlier integration work.
  - [ ] **Verify:** re-read `cei-labs-net/docs/security-qos-policy.md`
        and `network-topology.md`'s current port-range language and
        confirm it already covers: Bandit/Krypton's directly-published
        SSH ports (30000–32767, already documented), and the Natas
        attacker's port 22 (new, but same directly-published-port
        mechanism as any other `single-target`-style port, so likely
        already covered by the same range) plus its noVNC 6080 (Traefik,
        already documented as 80/443). If the SSH addition to
        `kali-novnc` changes how that specific port gets published
        (e.g. it's part of a `target-attacker` range rather than a
        `single-target`, which may use a different port-allocation path
        in the orchestrator) — confirm which allocation path it
        actually uses before concluding no firewall change is needed.
- [ ] Update `cei-labs-net/docs/ecosystem-architecture.md` with a short
      note (once built) that Bandit/Krypton/Natas are now self-hosted
      `single-target`/`target-attacker` instances rather than pointing at
      OverTheWire — documentation-only, reflecting reality.

## Phase 6 — Hardening & Size Pass (all new/changed images)

- [ ] Run each new image through the same discipline already established
      in `cei-labs-net/docker/docker-compose.yml`'s template: `cap_drop:
      ALL` plus only the specific capabilities a level's lesson actually
      needs back (e.g. a SUID-binary Bandit lesson may need
      `SETUID`/`SETGID` re-added — audit per level, don't blanket-grant),
      `no-new-privileges`, `pids_limit`, `mem_limit`, `cpus`.
  - [ ] **Verify:** for each image, attempt the specific privileged
        operation the lesson relies on with the proposed capability set
        and confirm it still works — don't drop a capability a level
        secretly needs and silently break it.
- [ ] `docker image ls` size check on every new/changed image — multi-
      stage builds to drop compilers/build tools; `apt-get clean && rm
      -rf /var/lib/apt/lists/*` in the same layer as every `apt-get
      install`; no stray package manager caches.
  - [ ] **Verify:** record the final size of each image (`bandit-target`,
        `krypton-target`, `natas-target`, updated `kali-novnc`) and
        sanity-check nothing is dramatically larger than its tool list
        would suggest (a bloated layer usually means a cache wasn't
        cleaned or a multi-stage build didn't actually drop the builder
        stage).
- [ ] Confirm non-root where the lesson allows it (Bandit/Krypton/Natas's
      whole mechanic is Unix user separation, so root is only used for
      setup/`sshd`/`apache2` master-process purposes — confirm that's the
      *only* root usage per image, not an oversight elsewhere).
- [ ] Read-only rootfs confirmed per image — final verification pass
      here, first implementation happened per-phase above.

## Phase 7 — Full Verification Pass (deploy and test for real, don't assume)

This phase re-confirms everything end to end, after all per-phase
verification above has already been done once during authoring — this is
the integration check, not the first time anything gets tested.

- [ ] Deploy a real `cei-labs-engine` stack locally (`docker swarm init`,
      `stack-up.sh`).
- [ ] Build and load all new/changed images with a `local-test`/`dev` tag
      (matching the established pattern from earlier testing):
      `bandit-target`, `krypton-target`, `natas-target`, updated
      `ctf-kali-novnc`.
- [ ] Sync the rewritten challenge YAML via `scripts/challenges-load.sh`.
- [ ] **As an actual player** (real exploitation, not flag-copying —
      this phase specifically exists to prove the mechanic, not the
      metadata):
  - [ ] Launch Bandit, SSH in as `bandit0`, solve at least 3
        representative levels spanning early/mid/late (a `find`-based
        level, a SUID level, a cron level) through the intended
        mechanism end to end.
  - [ ] Launch Krypton, solve all 7 levels (small enough to do
        exhaustively) through the intended decoding method each time.
  - [ ] Launch Natas, confirm the attacker box (both via SSH **and**
        via noVNC — test both access paths, not just one) can reach the
        target, and exploit at least 3 representative levels (e.g.
        view-source, a SQLi level, the file-upload level) end to end.
- [ ] Confirm `instance_group` sharing: opening two different
      Bandit-group challenges from the same team reuses the same
      container (check via `docker service ls` / orchestrator `GET
      /instances/...`, not just "it seemed to work").
- [ ] Confirm idle-timeout and `shutdown_on_solve`: solving the last
      level in a group starts the countdown (not earlier-level solves);
      the "+5 more minutes" extend action works.
- [ ] Confirm network isolation: from inside a Bandit/Krypton target,
      there is no route to any other team's instance, to CTFd, or to the
      orchestrator. From inside a Natas attacker, it can reach its own
      team's Natas target but not any other team's.
- [ ] Confirm inbound-port discipline: `nmap`/`docker port` each new
      container from outside its own network — Bandit/Krypton target:
      only 22; Natas attacker: only 22 and 6080; Natas target: nothing
      at all.
- [ ] Full teardown after verification, matching the established
      clean-up discipline from earlier phases of this project.

## Phase 8 — Rollout

- [ ] Commit Phase 2–4's new Dockerfiles + build-script changes to
      `CEI-Labs-Wargames`.
- [ ] Commit the `cei-labs-engine` `kali-novnc` SSH change from Phase 1.
- [ ] Commit the `cei-labs-net` documentation note from Phase 5.
- [ ] Re-run `deploy.sh` end to end one final time post-merge as the
      final go/no-go check before considering this done.

## Known open follow-ups (explicitly out of scope for this blueprint, noted so they aren't lost)

- The flags currently in `build_bandit.py`/`build_krypton.py`/
  `build_natas.py` were flagged earlier as looking like placeholder
  values — worth a content-accuracy pass, independent of this
  infrastructure work.
- The exact PHP version and any Natas-level-specific PHP behavior
  dependencies (e.g. an old PHP quirk a specific level's lesson relies
  on) hasn't been individually verified per level yet — flagged in
  Phase 4a as something to confirm while content-authoring, not deferred
  silently.
