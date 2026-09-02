# SSH login still shows Debian's boilerplate MOTD, not just the custom banner (2026-07-24)

Reported: SSH login to a target (Bandit/Krypton) should show only the
custom CEI Labs login message, nothing else — but Debian's standard
"Debian GNU/Linux..." boilerplate is also appearing. Notes only, no code
changed.

## This directly contradicts a prior investigation's conclusion — worth flagging explicitly

`cei-labs-engine/docs/HANDOFF-2026-07-23-night.md` §"ISSUE #5 — Standard
Debian MOTD... not shown" (2026-07-23) investigated the *opposite*
symptom — that the Debian text was **missing** — and concluded the fix
was to *enable* `PrintMotd yes` so it would show alongside the custom
banner. That doc's stated root cause: `PrintMotd no` in the target
sshd_config suppresses `/etc/motd` printing.

That conclusion turns out to be incomplete. Verified live against the
already-built `ghcr.io/stoptalkingishh/cei-labs-wargames/bandit:offline`
image:

```
$ grep -in 'printmotd\|usepam' /etc/ssh/sshd_config
85:UsePAM yes
94:PrintMotd no

$ cat /etc/motd
The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

$ grep -n motd /etc/pam.d/sshd
33:session    optional     pam_motd.so  motd=/run/motd.dynamic
34:session    optional     pam_motd.so noupdate
```

`PrintMotd no` only disables **OpenSSH's own** built-in MOTD-printing
code path. It does **not** disable PAM's separate `pam_motd.so` session
module, which independently prints `/etc/motd` on every login as long as
`UsePAM yes` is set (it is) and the module is active in `/etc/pam.d/sshd`
(it is, both lines uncommented). This is a well-known Debian/OpenSSH/PAM
gotcha — `PrintMotd no` alone looks like it should suppress the MOTD, but
PAM prints it anyway through a completely separate mechanism. So the
Debian legal text is, right now, actually printing at every login via
PAM — the opposite of what the night-of-2026-07-23 investigation
concluded, and exactly what's being reported now.

Also checked and ruled out as a source: `Banner` (sshd's pre-auth banner,
would print `/etc/issue.net`'s "Debian GNU/Linux 12" line before login)
is commented out (`#Banner none`), so that's not contributing anything
here.

## Where the custom banner itself comes from (for contrast, unaffected)

`targets/bandit/Dockerfile:88-96` installs
`/etc/profile.d/cei-bandit-banner.sh`, which `cat`s a per-user file under
`/etc/cei-labs/banners/`. This runs via bash's login-shell profile
sourcing, a completely separate mechanism from sshd/PAM's MOTD path — it
already works correctly and isn't part of this problem.

## What a fix would need

Not attempted here:

- Suppress PAM's MOTD printing too, not just sshd's — either disable both
  `pam_motd.so` lines in `/etc/pam.d/sshd` (comment out or remove), or
  truncate/empty `/etc/motd` at build time so pam_motd has nothing to
  print (simpler, doesn't touch PAM config directly, but a stray package
  upgrade repopulating `/etc/motd` later would silently reintroduce this).
- Apply to whichever targets actually use SSH login and PAM this way —
  confirmed present in `targets/bandit/`; `targets/krypton/` should be
  checked too (not verified in this pass) since it's also SSH-based;
  `targets/natas/` is HTTP-only and not applicable.
- Re-verify PAM behavior against a live SSH session (not just a
  `docker run --entrypoint sh` inspection of the files) before considering
  this closed — `docker exec`/non-interactive shells don't exercise the
  full sshd+PAM login path the way a real `ssh` connection does, so this
  is a strong signal but not a substitute for an actual login test.
