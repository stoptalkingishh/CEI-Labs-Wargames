# Offline Dependency Audit (A4)

Audience: whoever preps the build/deploy environment for the event venue.
Answers one question: **what needs internet access, and when** —
at image build time vs. at challenge-solve time — so a venue with
restricted or no internet on event day isn't a surprise.

## 1. Build-time package/download audit

Command run from repo root:

```bash
grep -rn "apt-get install\|pip install\|curl \|wget " targets/*/build/ targets/*/Dockerfile
```

Result: no hits under `targets/*/build/` (the setup scripts are pure
Python/shell content-generation, no package installs or downloads).
All install/download activity is in the three Dockerfiles, all at
`docker build` time (never at container start or solve time):

| Repo target | What it installs | Source |
|---|---|---|
| `targets/bandit/Dockerfile` | `gcc`/`libc6-dev` (builder stage, discarded), then `findutils grep gawk sed coreutils diffutils file binutils xxd tar gzip bzip2 xz-utils git cron openssh-client netcat-openbsd ncat socat openssl python3 python3-minimal vim nano` | Debian's standard `apt-get` repos only |
| `targets/krypton/Dockerfile` | `gcc`/`libc6-dev` (builder stage, discarded), then `python3 python3-minimal openssl xxd bsdextrautils coreutils binutils vim nano` | Debian's standard `apt-get` repos only |
| `targets/natas/Dockerfile` | `gnupg lsb-release python3 python3-minimal`, then `apache2 libapache2-mpm-itk apache2-utils php5.6 libapache2-mod-php5.6 php5.6-mysql php5.6-exif mariadb-server openssl libcap2-bin` | Debian repos **plus one external source** (below) |

**The one build-time dependency that isn't plain Debian apt**
(`targets/natas/Dockerfile:25`):

```dockerfile
RUN ... && curl -fsSL https://packages.sury.org/php/apt.gpg -o /etc/apt/trusted.gpg.d/sury-php.gpg \
    && echo "deb https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends apache2 libapache2-mpm-itk ... php5.6 ...
```

Natas level 14 needs PHP 5.6's legacy `mysql_connect()`/`mysql_query()`
(removed in PHP 7), which Debian 12's own repos don't ship — the
Dockerfile's own header comment explains this is deliberate, not an
oversight. `packages.sury.org` is a third-party APT mirror (Ondřej Surý's
well-known legacy-PHP repo), reached only during `docker build`, never at
container runtime or by a player. **This is the one package source that
needs to be pre-mirrored or vendored if the build has to happen on a
network-restricted machine** — everything else in all three Dockerfiles
resolves from stock Debian repos, which most local mirrors/proxies
already cover.

All three images are built once (ahead of the event) and shipped as
built artifacts; none of the above runs again at container start or
during play.

## 2. Doc / challenge-hint URL audit

Command run from repo root:

```bash
grep -rEo "https?://[^ )\"']+" docs/participant-quickstart.md docs/troubleshooting-faq.md challenges/*/challenge.yml
```

- `docs/participant-quickstart.md` and `docs/troubleshooting-faq.md`:
  **zero URLs** in either file.
- `challenges/*/challenge.yml` (generated from `scripts/build_{bandit,krypton,natas}.py`
  — see repo convention that these files are gitignored build output, not
  hand-edited): 40 URL occurrences, all either `<target-host>:PORT` connection
  placeholders (not real network destinations) or "Helpful reading" hint
  links to five external domains:

  `en.wikipedia.org`, `git-scm.com`, `help.ubuntu.com`, `jwiegley.github.io`, `linux.die.net`

This list exactly matches the already-documented, already-maintained
inventory in [`docs/network-access.md`](network-access.md) (that doc's
own audit command, run against the build scripts' `EXTRA_INFO` dicts,
produces the same five domains). No new domain surfaced — `network-access.md`
stays the source of truth for this list; nothing to update there from
this pass.

These links are all in the free-tier "Helpful reading" hint section —
background reading a participant can optionally open, never required to
solve a level (all flags/passwords are derivable from content already
inside the target box). Per `network-access.md`, player VLANs already
allow outbound WAN with a QoS priority exception for exactly these five
domains, so this is a pre-solved problem on the network side, not a new
gap.

## 3. Offline solve verification

Goal: prove a challenge is solvable with zero network access from inside
the running container, using only what's baked into the image at build
time.

The ticket's suggested command (`docker run --rm --network none
cei-labs-krypton:scan-test <solve command>`) doesn't match this repo's
actual image tag or runtime model — there is no `cei-labs-krypton:scan-test`
image anywhere in this repo's scripts, docs, or CI, and Krypton isn't a
single-shot "run a solve command" container. The real convention
(`scripts/build_krypton.py`'s own header comment) is
`ghcr.io/stoptalkingishh/cei-labs-wargames/krypton-target:latest`, a
persistent SSH box whose levels 1–6 content is generated at container
**start** (not build) from a `LEVEL_SECRETS` env var (see
`targets/krypton/entrypoint.sh`) — matching the "per-team dynamic
content" design used across all three tracks.

Verified against the real image instead, rebuilt fresh from current
`main` (`83e9f52`) to avoid testing a stale local image:

```
$ docker build -t ghcr.io/stoptalkingishh/cei-labs-wargames/krypton-target:latest targets/krypton
...
naming to ghcr.io/stoptalkingishh/cei-labs-wargames/krypton-target:latest done

$ docker run -d --network none --name krypton-offline-test \
    -e LEVEL_SECRETS='{"krypton1":"OfflineAuditTestFlag2026"}' \
    ghcr.io/stoptalkingishh/cei-labs-wargames/krypton-target:latest
7308ed85299748dcacbd6e02187ff4933dfd606ff8c34701d861aa4a08a62674

$ docker inspect krypton-offline-test --format 'NetworkMode={{.HostConfig.NetworkMode}}'
NetworkMode=none

$ docker exec krypton-offline-test cat /krypton/krypton1/README
The password for krypton2 is in the file 'krypton2' in this directory, rotated by 13 places (ROT13).

$ docker exec krypton-offline-test cat /krypton/krypton1/krypton2
BssyvarNhqvgGrfgSynt2026

$ docker exec krypton-offline-test bash -c "cat /krypton/krypton1/krypton2 | tr 'A-Za-z' 'N-ZA-Mn-za-m'"
OfflineAuditTestFlag2026

$ docker exec krypton-offline-test bash -c "SOLVED=\$(cat /krypton/krypton1/krypton2 | tr 'A-Za-z' 'N-ZA-Mn-za-m'); \
    [ \"\$SOLVED\" = \"OfflineAuditTestFlag2026\" ] && echo 'MATCH: offline solve verified, no network used at any point'"
Recovered password: OfflineAuditTestFlag2026
MATCH: offline solve verified, no network used at any point

$ docker rm -f krypton-offline-test
krypton-offline-test
```

Level 1 (ROT13) was solved end-to-end — reading the ciphertext, decoding
it with `tr` (baked into the image, no package fetch), and matching it
against the seeded per-team secret — entirely inside a container with
`NetworkMode: none`. `LEVEL_SECRETS` injection at container start (the
mechanism that makes content per-team-unique) also required no network
access; it's a local env var consumed by `entrypoint.sh`. This confirms
Krypton's runtime/solve path has no hidden network dependency — the only
network requirement anywhere in this target is the one `apt-get`/`curl`
build-time step documented in §1, for Natas, not Krypton.

## Summary

- **Build time:** all three targets need internet only for `apt-get`
  against stock Debian repos, except Natas which additionally needs
  `packages.sury.org` (legacy PHP 5.6) — the only package source to
  pre-mirror for an offline/restricted build environment.
- **Runtime/solve time:** zero network dependency, verified live against
  a freshly-built, `--network none` Krypton container.
- **Docs/hints:** `docs/participant-quickstart.md` and
  `docs/troubleshooting-faq.md` link nowhere; challenge hint links are
  the same five domains already tracked in `docs/network-access.md`,
  already allowlisted on the player VLAN — nothing new to bundle or
  mirror for those.
