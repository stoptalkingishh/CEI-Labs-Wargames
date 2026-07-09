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
| Natas | HTTP Basic Auth, `natasN.natas.labs.overthewire.org`, one PHP app per level | 34+ (0–33+) | **15** — curated subset (levels 0-14 only) | View-source, client-side-restriction bypass, directory listing, robots.txt, Referer-header spoofing, cookie auth bypass, source disclosure, LFI, encoding puzzle, command injection (x2), XOR cookie forgery, file upload (x2), SQLi — see the per-level table in Phase 4a |

**This is a scoped job**: self-host what's already authored (34 + 7 + 15 =
56 challenges, already live in CTFd per earlier testing), not expand to
OTW's full upstream catalog. Both Bandit and Krypton are, in reality,
**one single shared machine per player** that you progress through by
escalating to the next level's user — not 34 (or 7) separate machines.
Natas is, in reality, **one single web server** hosting many vhosts, with
per-level Unix users controlling which password files are readable from
which level.

### Research methodology (how the facts below were actually gathered)

Two sources, used deliberately in this order:

1. **Limited, passive-only direct interaction with OTW's live Natas
   server**, using OTW's own published, intended starting credentials
   (`natas0`/`natas0`) — explicitly bounded to viewing responses/page
   source, exactly what each level's own instructions say to do. This
   confirmed real infrastructure facts no write-up states explicitly:
   `Server: Apache/2.4.66 (Ubuntu)` (from response headers), the exact
   static HTML/CSS/JS scaffold OTW wraps every level in (including a
   `wechall` integration explicitly commented as "nothing to do with the
   level" — noise to ignore when designing our own version), and
   `mod_autoindex` directory-listing behavior on natas2 confirmed live
   rather than assumed from a write-up. This stopped at natas2: the
   session's own safety controls flagged fetching the actual
   directory-listing-discovered file as crossing from "view what the
   level shows you" into "perform the exploitation step against a live
   third-party system," and declined it — a stricter line than this
   plan had drawn for itself, respected rather than argued with. No
   further live levels were attempted past that point.
2. **Community write-ups for everything else** (levels 3-14's specific
   mechanisms, the PHP version implications) — the primary, scalable
   source for this research, cross-checked across multiple independent
   write-ups per level rather than trusting a single source, per
   instruction. This is standard practice for a wargame OTW has
   published openly and encourages solving; every technique below is
   publicly documented by numerous independent solvers, not discovered
   through any original probing of OTW's infrastructure.

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

## Phase 1 — Base Image Work (cei-labs-engine) — ✅ COMPLETE (2026-07-08)

Branch: `feature/self-hosted-wargames-base-images` (not yet merged to
`main`, not yet pushed — local commit pending). All items below actually
built and tested locally, not just planned.

- [x] **`operator/kali-novnc/Dockerfile`**: added `openssh-server` to the
      `apt-get install` list; `mkdir -p /var/run/sshd` + `ssh-keygen -A`;
      `PasswordAuthentication yes` / `PermitRootLogin no` set explicitly
      in `sshd_config`; same `operator` user/password already used for
      VNC now also works for SSH — no second credential.
  - [x] **Verified:** built and ran the image standalone. `sshd` starts
        cleanly alongside VNC/noVNC — confirmed via `ps aux` showing all
        5 expected processes (`Xtigervnc`, `xfce4-session`,
        `dbus-launch`, `websockify`, `sshd`), healthcheck reporting
        `healthy`.
  - [x] **Verified:** `EXPOSE 22` added alongside `EXPOSE 6080`; both
        confirmed present via `docker inspect`.
  - [x] **Verified:** SSH login as `operator` with the exact same
        password used for VNC succeeded (tested via a scripted client,
        not just "should work") — confirms one genuinely shared
        credential across both protocols.
  - [x] **Verified noVNC still works** — didn't just add SSH and assume
        the existing path was untouched; `curl`'d the noVNC web root and
        got `200`.
  - [x] **Two pre-existing bugs found and fixed along the way** (both
        unrelated to the SSH work — confirmed by building the
        *unmodified* Dockerfile from `main` and reproducing both
        failures there first, before concluding they weren't something
        this change introduced):
    1. **TigerVNC config path**: `kalilinux/kali-rolling:latest` now
       ships a TigerVNC version that uses the XDG-compliant
       `~/.config/tigervnc/` path instead of the legacy `~/.vnc/`, and
       its auto-migration between the two fails outright in this
       environment (`vncserver: Could not migrate ... to
       .../.config/tigervnc`). Fixed by writing `xstartup`/`passwd`
       directly to `~/.config/tigervnc/` instead of `~/.vnc/`, bypassing
       the broken migration path entirely.
    2. **`xstartup` exits too early**: the original script backgrounded
       the window manager (`xfce4-session &`) and returned immediately;
       current TigerVNC treats an xstartup script returning that fast as
       "session exited too early" and tears the whole server down.
       Fixed by running `exec xfce4-session` in the foreground instead.
    This means **`kali-novnc` was completely non-functional on `main`**
    against the current Kali rolling base before this session — not a
    hypothetical, reproduced twice (build-from-`main`, then build with
    only the SSH diff applied, same failure both times) and fixed as
    part of this same branch. Important since this image is also the
    Natas attacker for Phase 4 — would have silently blocked that phase
    too if left unfound.
- [x] Confirmed `operator/targets/base-linux` needs **no changes** for
      Bandit/Krypton. Built it standalone and checked directly (not
      assumed): Debian's `openssh-server` package auto-generates SSH host
      keys via its own postinst script at `apt-get install` time — no
      explicit `ssh-keygen -A` needed here (unlike the Kali-rolling image
      above, where it's needed explicitly) — `sshd -t` reported the
      config valid immediately after build.
- [x] **Read `scripts/challenges-load.sh` in full — field names
      confirmed exactly as planned:** `instance_type`, `image`, `port`,
      `target_image`, `attacker_image`, `attacker_port`,
      `instance_group`, `shutdown_on_solve` (default `true`) — all
      present, all matching `InstanceChallengeConfig`'s columns. No
      adjustment needed to Phase 2-4's planned YAML field names.
  - [x] **New finding, not previously known — changes Phase 5's scope:**
        `challenges-load.sh` only syncs `instance_type` metadata for
        challenge YAML living under **`cei-labs-engine`'s own**
        `challenges/sprint{1,2,3}-*/` directories, via a
        `sync_instance_mapping()` function that POSTs to
        `/plugins/instance-launcher/admin/mappings/sync`, authenticated
        with the `plugin_shared_secret` Docker secret.
        **`CEI-Labs-Wargames`' own `deploy.sh` has no equivalent step at
        all** — it only calls plain `ctf challenge push`/`sync`/`install`
        (via `ctfcli`), which populates ordinary CTFd challenge fields
        (name/description/flags/value/category) but has no concept of
        `instance_type` and never touches the instance-launcher plugin's
        mapping table. **Consequence: adding `instance_type`/
        `instance_group`/etc. to `build_bandit.py` et al.'s generated
        YAML, as Phase 2-4 plan to, will silently do nothing** (no
        "Launch Environment" button appears) unless `deploy.sh` also
        gets its own version of `sync_instance_mapping()`. Moved to
        Phase 5 as a concrete, now-necessary task — see below.
  - [x] **RESOLVED (2026-07-08):** decided to scrub, not merge or keep
        both. Removed `challenges/sprint1-otw/` (15-level partial Bandit
        duplicate + a "Sprint 1 Complete" gate marker),
        `challenges/sprint2-web/` (the 2 "OTW Natas" stubs + Juice Shop
        entries), and `challenges/sprint3-pccc/` (crAPI/PCCC content)
        from `cei-labs-engine` entirely — branch
        `feature/self-hosted-wargames-base-images` @ `d1e8fff`.
        Rationale: `cei-labs-engine` is a platform, not a content
        author — all challenge content belongs in dedicated wargames
        repos (`CEI-Labs-Wargames` for Bandit/Krypton/Natas). Confirmed
        safe before removing: `scripts/challenges-load.sh`'s
        `load_sprint()` already handles a missing directory gracefully
        (warns and skips, doesn't error — read the source to confirm,
        didn't assume), and the repo's CI (`validate.yml`) walks the
        whole tree generically for YAML syntax checking, no hardcoded
        path dependency on the removed directories. Updated
        `README.md`'s Training Tracks intro, Quick Start step 4, and
        the Event Readiness Roadmap to reflect that challenge content
        is sourced externally now.

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
- [ ] **PHP version — resolved, not a placeholder.** Researched and
      confirmed: real Natas's SQLi-relevant levels (14, and 15/17 just
      beyond our scope) use `mysql_connect()`/`mysql_query()`/
      `mysql_close()` — the **old `ext/mysql` extension, removed entirely
      in PHP 7.0**. This isn't cosmetic; that function family simply does
      not exist on any PHP 7+ install, so faithfully reproducing this
      level's exact code requires a genuinely legacy PHP. This is the
      concrete case behind "we'll likely need older systems/services,"
      confirmed rather than assumed. **Install PHP 5.6** (last PHP 5.x
      release) via the `sury.org`/`ondrej/php`-style legacy-PHP APT
      repository, layered on top of the same `debian:12-slim` base —
      confirmed viable in 2026 (this is the standard, still-maintained
      path for exactly this "old PHP on a current base OS" need; using
      it keeps one base-OS family project-wide instead of reaching for a
      different, older distro just for Natas). Install
      `php5.6-mysql` alongside base `php5.6`/`libapache2-mod-php5.6`.
  - [ ] **Verify:** `php5.6 -m` inside the built image lists `mysql`
        (the legacy extension, distinct from `mysqli`/`pdo_mysql`);
        confirm `mysql_connect()` is actually callable, not just that
        the package installed without error.
  - [ ] **Verify:** `apache2ctl -M` inside the built image lists `mpm_itk`
        as the active MPM (not `prefork`/`event`/`worker` — MPM-ITK
        replaces the MPM entirely, it isn't a bolt-on module; confirm no
        conflicting MPM package got pulled in as a dependency) **and**
        that PHP 5.6 (not any Debian-12-default PHP that may have been
        pulled in as a dependency of something else) is the version
        actually executing — `phpinfo()` on a throwaway test vhost during
        the build, removed before shipping.
  - [ ] **Risk flagged, not hidden:** genuinely running PHP 5.6 means
        running an interpreter with known, public, unpatched CVEs by
        design — that's the point of a CTF target, not an oversight. The
        Phase 4a "no externally published port at all" isolation (below)
        and Phase 6 hardening are what make this safe to run: the target
        has no reachability from anywhere except its own team's attacker,
        so PHP 5.6's *other*, unintended vulnerabilities can't be
        leveraged for anything beyond that single isolated pair.
      Add `mariadb-server` in the same container for simplicity, since
      this is a single-purpose disposable-per-team box, not a shared
      service — no need for a separate DB container the way
      `cei-labs-engine` does for CTFd's own DB.
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
- [ ] Content-author each of the 15 vulnerability lessons. **Correction
      to earlier draft:** "PHP object injection" was in this blueprint's
      first pass because it's part of Natas's general topic range —
      research now confirms that's real Natas level 25-26, well beyond
      the 0-14 subset actually authored in this repo (confirmed level 14
      = SQLi, matching what `build_natas.py`'s sync log already showed:
      "Natas 14 -> 15: SQL Injection (SQLi)"). **Object injection is out
      of scope for these 15 levels** — remove it from the topic list;
      don't build content for it.

      Researched, per-level technical reference for what natas0-natas14
      actually teach (independent write-ups cross-checked against each
      other, not a single source) — build each level's PHP/Apache config
      to match this mechanism specifically, not just the category name:

      | Level | Mechanism to recreate |
      | :--- | :--- |
      | 0 | Password sits in an HTML comment in the page source — pure "view source" lesson, no PHP logic needed. |
      | 1 | Same as 0, but `oncontextmenu` JS blocks right-click — the lesson is knowing `view-source:` or devtools bypasses client-side-only restrictions. Password still just an HTML comment. |
      | 2 | Page references `files/pixel.png`; Apache directory listing (`mod_autoindex`) is left on for `/files/`, exposing an unlinked `users.txt` alongside it. Requires `Options +Indexes` on that one directory. |
      | 3 | `/robots.txt` has a `Disallow:` entry pointing at a hidden directory that itself has directory listing on, containing a `users.txt`. Lesson: robots.txt tells you what NOT to crawl, which is exactly what a human should check. |
      | 4 | Page checks the `Referer` header and only shows the password if it equals this same level's own URL — trivially forgeable client-side header, lesson is that `Referer` is not an auth mechanism. |
      | 5 | Cookie `loggedin=0`; page logic is `if ($_COOKIE['loggedin'] == 1) { show password }` — classic client-trusted-cookie auth bypass. |
      | 6 | Page provides an explicit "View sourcecode" link (**intentional feature, not a bug** — several early levels are meant to teach reading PHP before finding bugs). Source reveals a form comparing user input against a `$secret` value defined in a separate `includes/secret.inc` file — also fetchable directly since it's still under the webroot, revealing the secret. |
      | 7 | `?page=` parameter is used in a PHP `include`/`require` without sanitization — classic LFI, path-traversal to `/etc/natas_webpass/natas8`. |
      | 8 | An `encodeSecret()` function chains `base64_encode` → `strrev` → `bin2hex`; page shows the *encoded* result and asks for the plaintext that would encode to it — lesson is reversing a simple, discoverable (source is visible) encoding chain, not real cryptography. |
      | 9 | Page runs `passthru("grep -i $key dictionary.txt")` with `$key` taken straight from user input, no escaping — direct OS command injection via shell metacharacters. |
      | 10 | Same `grep` pattern as 9, but `preg_match('/[;|&]/', $key)` blocks the obvious shell metacharacters — lesson is that `grep` itself accepts a second filename argument, so injecting *arguments* (not shell operators) still achieves arbitrary file read without needing a blocked character. |
      | 11 | State is stored in a cookie XOR-encrypted with a short repeating key; the *default* (logged-out) plaintext is known (`array("showpassword"=>"no","bgcolor"=>"#ffffff")`), so `known_plaintext XOR ciphertext = key` recovers the key, letting you forge a cookie with `showpassword=yes`. |
      | 12 | Upload form only checks the client-supplied filename's extension (not real content), and saves+serves uploaded files as-is — upload a `.php` file containing a one-line web shell, then request it to execute arbitrary PHP (e.g. reading the next password file). |
      | 13 | Same upload flow as 12, but adds an EXIF/`getimagesize()`-style check on the file's actual bytes — bypassed by prepending real JPEG magic bytes/header before the PHP payload, since PHP doesn't care what precedes `<?php` as long as it's still valid to execute. |
      | 14 | Login form builds `SELECT * FROM users WHERE username="<input>" AND password="<input>"` via raw string concatenation into `mysql_query()` (the PHP 5.6 legacy extension from above) — classic SQLi, e.g. `" OR ""="` in either field bypasses the check entirely. This is the level that anchors the whole PHP-version requirement. |

  - [ ] **Verify per level as authored:** actually exploit it yourself
        (or delegate a full pass to the Phase 7 playthrough, but at
        minimum smoke-test each as it's written) — confirm the intended
        vulnerability is present, exploitable via the intended technique
        from the table above, and yields the next level's access/password
        through that technique specifically, not through some unintended
        shortcut.
  - [ ] **Verify against the repo, not just against research:** before
        finalizing each level's implementation, cross-check this table's
        mechanism against what `build_natas.py`'s actual existing
        description/flag for that level implies — if any level's already-
        authored content clearly describes a different mechanism than the
        table above, the repo's own content wins; treat a mismatch as a
        signal to re-read that specific level's write-ups more carefully,
        not to silently override the repo.
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

- [x] **DONE (2026-07-08):** added `sync_instance_mapping()` to
      `CEI-Labs-Wargames/deploy.sh` (branch `feature/self-hosted-wargames`
      @ `1e1ff23`), mirroring `challenges-load.sh`'s function of the same
      name — same payload shape, same endpoint, same header. Reads the
      shared secret from a `CTFD_SYNC_SECRET` env var (opt-in, backward
      compatible — unset behaves exactly as before) instead of a local
      secrets file, since this repo isn't colocated with
      `cei-labs-engine`'s `docker/secrets/`.
  - [x] **Verified for real, not just written:** posted a real payload
        for an already-synced challenge against the actual running local
        CTFd — got a 403 on the first attempt.
  - [x] **New bug found and fixed as a result — genuinely load-bearing,
        affects `challenges-load.sh` too, not just this new caller:**
        `/plugins/instance-launcher/admin/mappings/sync` had no CSRF
        exemption, so CTFd's global CSRF check rejected every call before
        the route's own `X-Sync-Auth` check ever ran — this route had
        apparently never been exercised end-to-end before now. Fixed in
        `cei-labs-engine` (branch `feature/self-hosted-wargames-base-images`
        @ `e3e6350`) with CTFd's own documented mechanism for exactly this
        case, `@bypass_csrf_protection` — confirmed via CTFd's own source
        this only exempts the session-based CSRF nonce, not the route's
        actual `X-Sync-Auth` access control, which is unchanged.
  - [x] **Verified after the fix:** rebuilt and redeployed the local CTFd
        image, re-posted the same payload — `HTTP 200`, and confirmed via
        a **direct query against the `instance_launcher_configs` table**
        (not just trusting the API response) that a real row landed with
        the exact posted values.
  - [x] **Incidental finding, noted not fixed:** hit a separate,
        unrelated build failure while rebuilding the CTFd image —
        `docker/ctfd/docker-entrypoint-wrapper.sh` had CRLF line endings
        in this local Windows checkout (breaking its shebang inside the
        Linux container), caused by `git checkout -b` + Windows Git's
        default `core.autocrlf` with no `.gitattributes` forcing LF for
        shell scripts. Confirmed the repo's actual stored content is LF
        (no diff after stripping `\r` locally) — this is a checkout-time
        risk for any Windows contributor, not a repo content bug. Worth a
        `.gitattributes` (`*.sh text eol=lf`) at some point; not blocking,
        not done here.
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

- **Natas scope confirmed as a deliberate decision (2026-07-08), not a
  gap:** this blueprint self-hosts exactly the 15 already-authored levels
  (0-14). Levels 25-26 (PHP Object Injection) and the rest of real Natas's
  34+ level catalog are explicitly **not** part of this build. If that
  ever changes, it's a distinct future project — new content authoring in
  `CEI-Labs-Wargames` (new CTFd challenges, new vhosts/users on the Natas
  target image, extending the same MPM-ITK/PHP-5.6 pattern this blueprint
  already establishes) — not a correction to this one. Revisit this
  blueprint's scope table (top of file) if/when that's greenlit.
- The flags currently in `build_bandit.py`/`build_krypton.py`/
  `build_natas.py` were flagged earlier as looking like placeholder
  values — worth a content-accuracy pass, independent of this
  infrastructure work.
- The exact PHP version and any Natas-level-specific PHP behavior
  dependencies (e.g. an old PHP quirk a specific level's lesson relies
  on) hasn't been individually verified per level yet — flagged in
  Phase 4a as something to confirm while content-authoring, not deferred
  silently.

## Research sources

Official:
- [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/)
- [OverTheWire: Krypton](https://overthewire.org/wargames/krypton/)
- [OverTheWire: Natas](https://overthewire.org/wargames/natas/)

Natas per-level mechanisms (cross-checked across multiple independent
write-ups per level, per the level table in Phase 4a):
- [[OTW] Write-up for the Natas Wargame — BreakInSecurity](https://axcheron.github.io/writeups/otw/natas/)
- [OverTheWire Natas Level 5 Solution — Medium](https://greenorangge1.medium.com/overthewire-natas-level-5-7a2a3a208ed1)
- [OverTheWire: Natas Level 3→4 — jsinix](https://medium.com/overthewire-natas-writeup-by-jsinix/overthewire-natas-level-3-level-4-984c608aaf4)
- [OverTheWire: Natas Level 6→7 — jsinix](https://medium.com/overthewire-natas-writeup-by-jsinix/overthewire-natas-level-6-level-7-c0bd8af915d7)
- [OverTheWire Natas Level 0–11 — Medium](https://medium.com/@kiddosz/overthewire-natas-level-0-level-11-cac088c41f09)
- [OverTheWire: 'Natas' Solutions 11-15 — jhalon](https://jhalon.github.io/over-the-wire-natas2/)
- [SQL Injection — Bypassing Double Quotes — Natas Level 14 — Motasem Hamdan](https://motasem-notes.net/sql-injection-bypassing-double-quotes-overthewire-natas-level-14/)
- [OvertheWire Natas 1 To 34 Full Writeup — CertCube](https://blog.certcube.com/overthewire-natas/)
- [OverTheWire: Natas Level 25→26 (PHP Object Injection, real level ~25-26, confirmed out of scope for our 0-14 subset) — jsinix](https://medium.com/overthewire-natas-writeup-by-jsinix/overthewire-natas-level-25-26-a2661a5b17ea)
- [OverTheWire – natas22,24-26 – Ivan's IT learning blog](https://ivanitlearning.wordpress.com/2020/02/02/overthewire-natas2224-26-more-php-fun/)

Krypton per-level topics:
- [OverTheWire Krypton (Levels 0-9) — LearnHacking.io](https://learnhacking.io/overthewire-krypton-levels-0-9/)
- [[OTW] Write-up for the Krypton Wargame — BreakInSecurity](https://axcheron.github.io/writeups/otw/krypton/)

PHP 5.6 / legacy `mysql_*` extension on a current base OS:
- [Docker file for PHP 5.6 with Apache, MySQL extension — GitHub Gist](https://gist.github.com/guibranco/9342f83c5e51b7ec85d9046c652d1074)
- [Dockerizing Legacy PHP Apps: A Step-by-Step Migration Guide — DoHost](https://dohost.us/index.php/2026/03/26/dockerizing-legacy-php-apps-a-step-by-step-migration-guide/)

Apache MPM-ITK (per-vhost `AssignUserID`):
- [apache2-mpm-itk — official project page](http://mpm-itk.sesse.net/)
- [Debian package: libapache2-mpm-itk](https://packages.debian.org/search?keywords=libapache2-mpm-itk)
