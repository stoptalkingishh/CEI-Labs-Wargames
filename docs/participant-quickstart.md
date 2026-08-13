# Participant Quick-Start

Everything you need to get going, in one page. No prior CTF experience
assumed.

## 1. Log in

Use the account/credentials given to you at the start of the event. If
you don't have one yet, ask an instructor.

## 2. Find "Start Here"

Each of the three tracks — **Bandit** (Linux basics), **Krypton**
(cryptography), **Natas** (web security) — has one challenge literally
named "**\<Track\>: Start Here**". Open that first, even if you're
experienced — it walks you through the track's specific connection
method, since they're not all the same:

- **Bandit and Krypton** connect you directly via SSH to a shared
  target box.
- **Natas** is different: when your event operator has made it available,
  launching gives you a shared **attacker workstation** first, and every
  Natas target is only reachable from *inside* that workstation — never
  directly from your own machine.

## 3. Use the Launch panel

Every challenge that needs an environment has a launch control attached
to its description in CTFd. Click **Launch Environment** — after a
short wait, you'll get connection info (host/port, and for Natas, links
to the attacker workstation).

- **Reboot Host** — restarts your environment in place if it gets
  stuck. Doesn't lose your progress on the challenge itself.
- **Relaunch Environment** — tears down and rebuilds your whole
  environment from scratch. Use this if a reboot doesn't fix it.
- On shared-box tracks (Bandit, Krypton), you only need to launch once —
  every level after the first one in that track reuses the same
  environment automatically.

**For Natas specifically:** use the **noVNC** link supplied by your event
operator (a full desktop in your browser). It is the supported participant
path. Do not assume SSH access exists or try to infer a login; use SSH only
if the event operator explicitly gives you a tested endpoint and credential.
See [`natas-completion-status.md`](natas-completion-status.md) for the
deployment prerequisite behind this path.

## 4. Read the description carefully

Every challenge's description includes a free **"Commands you may need"**
and **"Helpful reading"** section — pointers to the exact tools and
background concepts involved, given up front, before you spend any
points on hints.

## 5. Use hints if you're stuck

Every level has up to 3 hint tiers, each costing more points than the
last:

1. **Tier 1** — a bare pointer (a command name or a single reading
   link). For when you just need reminding what tool applies here.
2. **Tier 2** — a real explanation of the concept, still leaving you to
   work out the exact command yourself.
3. **Tier 3** — a full step-by-step walkthrough of the technique.

Using a hint costs points but never fails the challenge or blocks you
from solving it normally — it's a trade-off, not a penalty.

## 6. Submit the flag

Flags go in the challenge's submission box on CTFd, exactly as shown by
the target (case matters).

## Where to get help

- Stuck on a puzzle? Try the next hint tier first.
- Something looks actually broken (not just hard)? Ask an instructor —
  don't assume it's a bug in the challenge itself; a lot of "this isn't
  working" turns out to be a normal part of the puzzle (e.g., a
  restricted shell that's *supposed* to reject your first few attempts).
- Environment seems stuck or unresponsive? Try **Reboot Host** first,
  then ask an instructor if that doesn't help.
