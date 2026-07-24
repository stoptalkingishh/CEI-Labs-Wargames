#!/bin/bash
# Starts every level's background daemon (port listeners for levels
# 14-24ish -- see /opt/bandit-daemons/) and the cron daemon (levels
# 21-23's lessons depend on it actually firing on schedule), then execs
# sshd in the foreground as PID 1's replacement. Port-listener daemons
# run as the unprivileged `banditd` user, never as root or as any
# bandit* player account; cron necessarily runs as root (it's what lets
# it su into each level's own user per /etc/cron.d's user field), same
# trust level as sshd itself.
#
# Per-team secrets: most levels' flags/passwords ARE generated here, at
# container START, from $LEVEL_SECRETS (a JSON blob the orchestrator
# injects -- see cei-labs-engine's instance_types.py
# generate_fixed_length_track_secrets(), used for every Bandit level
# since several levels' static descriptions are calibrated to an exact
# byte count/position). bandit0's password stays the real, public
# "bandit0" -- OverTheWire's well-known bootstrap credential, not a
# secret. If a level's key is missing from $LEVEL_SECRETS (e.g. CTFd
# content hasn't been synced yet), that level's account is simply left
# with no usable password and its content stays as an inert placeholder
# -- a safe failure mode, not a shared-credential one. Level 13's SSH
# keypair (bandit13 -> bandit14) is generated fresh here too, per
# container/team, same as everything else -- see docs/security-audit-status.md.
set -e

if [ -n "${LEVEL_SECRETS:-}" ]; then
    python3 - <<'PYEOF'
import base64
import bz2
import codecs
import gzip
import json
import os
import subprocess

secrets = json.loads(os.environ.get("LEVEL_SECRETS", "{}"))


def placeholder(n: int) -> str:
    return f"BANDITPLACEHOLDER{n:02d}".ljust(32, "Z")


# ---- Login password chain: bandit(n+1)'s password = bandit-n's flag ----
for n in range(0, 33):
    flag = secrets.get(f"bandit{n}")
    if not flag:
        continue
    subprocess.run(["chpasswd"], input=f"bandit{n+1}:{flag}\n", text=True, check=True)

# ---- Simple placeholder substitution: flag written plain into a file --
CONTENT_SUBS = {
    "/home/bandit0/readme": (placeholder(0), "bandit0"),
    "/home/bandit1/-": (placeholder(1), "bandit1"),
    "/home/bandit2/spaces in this filename": (placeholder(2), "bandit2"),
    "/home/bandit3/inhere/.hidden": (placeholder(3), "bandit3"),
    "/home/bandit4/inhere/-file07": (placeholder(4), "bandit4"),
    "/home/bandit5/inhere/maybehere13/.file2": (placeholder(5), "bandit5"),
    "/var/lib/bandit-data/.sys-cache-6f2a": (placeholder(6), "bandit6"),
    "/home/bandit7/data.txt": (placeholder(7), "bandit7"),
    "/home/bandit8/data.txt": (placeholder(8), "bandit8"),
    "/home/bandit9/data.txt": (placeholder(9), "bandit9"),
    "/etc/bandit_pass/bandit14": (placeholder(13), "bandit13"),
    "/home/bandit17/passwords.new": (placeholder(17), "bandit17"),
    "/home/bandit18/readme": (placeholder(18), "bandit18"),
    "/etc/bandit_pass/bandit20": (placeholder(19), "bandit19"),
    "/etc/bandit_pass/bandit22": (placeholder(21), "bandit21"),
    "/etc/bandit_pass/bandit23": (placeholder(22), "bandit22"),
    "/etc/bandit_pass/bandit24": (placeholder(23), "bandit23"),
    "/home/bandit25/readme": (placeholder(25), "bandit25"),
    "/home/bandit26/.hidden_dir/flag_26": (placeholder(26), "bandit26"),
    "/home/bandit32/.creds/flag": (placeholder(32), "bandit32"),
    "/home/bandit33/.final/flag": (placeholder(33), "bandit33"),
}
for path, (token, key) in CONTENT_SUBS.items():
    value = secrets.get(key)
    if not value or not os.path.exists(path):
        continue
    with open(path, "rb") as f:
        content = f.read()
    with open(path, "wb") as f:
        f.write(content.replace(token.encode(), value.encode()))

# ---- Level 13: bandit13's SSH keypair that logs into bandit14 --
# generated fresh per container (i.e. per team) here, instead of once at
# image BUILD time, closing the team-isolation gap noted in
# docs/security-audit-status.md: every team's image used to bake in the
# exact same keypair, so any team that reached level 13 could also SSH
# straight into every OTHER team's bandit14 with it -- not just read its
# own. Guarded by os.path.exists() on the private key so a Reboot (same
# container, filesystem not wiped -- see the levels-27-31 comment below)
# doesn't silently swap out a player's already-downloaded sshkey.private
# for a new, non-matching key.
bandit13_key = "/home/bandit13/sshkey.private"
if not os.path.exists(bandit13_key):
    tmp_key = "/tmp/bandit13-14-key"
    subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-N", "", "-C", "bandit14-access", "-f", tmp_key],
        check=True,
    )

    subprocess.run(["install", "-m", "700", "-o", "bandit13", "-g", "bandit13", "-d", "/home/bandit13/.ssh"], check=True)
    subprocess.run(["install", "-m", "600", "-o", "bandit13", "-g", "bandit13", tmp_key, bandit13_key], check=True)

    subprocess.run(["install", "-m", "700", "-o", "bandit14", "-g", "bandit14", "-d", "/home/bandit14/.ssh"], check=True)
    subprocess.run(
        ["install", "-m", "600", "-o", "bandit14", "-g", "bandit14", f"{tmp_key}.pub", "/home/bandit14/.ssh/authorized_keys"],
        check=True,
    )

    os.remove(tmp_key)
    os.remove(f"{tmp_key}.pub")

# ---- Level 20: suconnect's expected/next passwords, read from a runtime
# config file instead of compiled into the binary (see
# src/level20_suconnect.c) -- owned bandit21:bandit21, mode 0400, so it's
# readable ONLY while the SUID binary's effective UID is bandit21, never
# directly by bandit20 via cat/find, preserving the original design's
# security boundary.
flag19 = secrets.get("bandit19")
flag20 = secrets.get("bandit20")
if flag19 and flag20:
    with open("/etc/bandit21_suconnect.conf", "w") as f:
        f.write(f"{flag19}\n{flag20}\n")
    subprocess.run(["chown", "bandit21:bandit21", "/etc/bandit21_suconnect.conf"], check=True)
    os.chmod("/etc/bandit21_suconnect.conf", 0o400)

# ---- Levels 10/11/12: flag is transformed, so it's regenerated fresh --
# (no build-time file exists at all for these 3 -- unlike CONTENT_SUBS
# above, there's nothing to gate on os.path.exists() for).
# Owned by the NEXT level's user, group-owned by the current level's user,
# mode 0640 -- same bandit7:bandit6 pattern as level 6 (and levels 0-9
# above): the current level's own player reads it via the group bit while
# solving the level, but it's not world-readable so no one else can skip
# straight to it.
flag10 = secrets.get("bandit10")
if flag10:
    with open("/home/bandit10/data.txt", "wb") as f:
        f.write(base64.b64encode(flag10.encode()) + b"\n")
    subprocess.run(["chown", "bandit11:bandit10", "/home/bandit10/data.txt"], check=True)
    os.chmod("/home/bandit10/data.txt", 0o640)

flag11 = secrets.get("bandit11")
if flag11:
    with open("/home/bandit11/data.txt", "w") as f:
        f.write(codecs.encode(flag11, "rot13") + "\n")
    subprocess.run(["chown", "bandit12:bandit11", "/home/bandit11/data.txt"], check=True)
    os.chmod("/home/bandit11/data.txt", 0o640)

flag12 = secrets.get("bandit12")
if flag12:
    compressed = bz2.compress(gzip.compress(flag12.encode()))
    hex_lines = subprocess.run(["xxd", "-"], input=compressed, capture_output=True, check=True).stdout
    with open("/home/bandit12/data.txt", "wb") as f:
        f.write(hex_lines)
    subprocess.run(["chown", "bandit13:bandit12", "/home/bandit12/data.txt"], check=True)
    os.chmod("/home/bandit12/data.txt", 0o640)

# ---- Levels 27-31: five git-shell service accounts, each serving one
# bare repo whose history/branches/tags/hooks hide the next level's
# password -- moved here from a Dockerfile-build-time script entirely
# (docs/security-audit-status.md), since each team needs its own
# distinct repo content. Skips entirely if bandit27-git already exists --
# a Reboot (not a full Relaunch) restarts this SAME container without
# wiping its filesystem, and the secrets are stable for a container's
# whole lifetime, so redoing this on every restart would be redundant
# (useradd on an already-existing user would also just error under `set
# -e`, which this guard avoids needing to handle piecemeal).
import pwd

try:
    pwd.getpwnam("bandit27-git")
    _git_levels_already_set_up = True
except KeyError:
    _git_levels_already_set_up = False

git_pw = {n: secrets.get(f"bandit{n-1}") for n in (27, 28, 29, 30, 31)}
git_flag = {n: secrets.get(f"bandit{n}") for n in (27, 28, 29, 30, 31)}

if not _git_levels_already_set_up and all(git_pw.values()) and all(git_flag.values()):
    TMP = "/tmp/bandit-git-setup"
    GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="CEI Labs", GIT_AUTHOR_EMAIL="build@cei-labs.local",
                   GIT_COMMITTER_NAME="CEI Labs", GIT_COMMITTER_EMAIL="build@cei-labs.local")

    def git_run(cmd, cwd=None):
        subprocess.run(cmd, cwd=cwd, env=GIT_ENV, check=True,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def git_write(path, content):
        with open(path, "w", newline="\n") as f:
            f.write(content)

    def create_git_shell_account(n):
        user = f"bandit{n}-git"
        subprocess.run(["useradd", "-m", "-s", "/usr/bin/git-shell", "--no-log-init", user], check=True)
        subprocess.run(["chpasswd"], input=f"{user}:{git_pw[n]}\n", text=True, check=True)

    def init_bare(path):
        os.makedirs(path, exist_ok=True)
        git_run(["git", "init", "-q", "--bare", path])

    for n in (27, 28, 29, 30, 31):
        create_git_shell_account(n)

    os.makedirs(TMP, exist_ok=True)

    # Level 27: password sitting in a file at HEAD.
    bare27 = "/home/bandit27-git/repo"
    init_bare(bare27)
    work = f"{TMP}/w27"
    git_run(["git", "init", "-q", "-b", "master", work])
    git_write(f"{work}/README.md",
              "Bandit level 27\n================\n\n"
              f"You found me! The password for the next level is:\n\n{git_flag[27]}\n")
    git_run(["git", "add", "README.md"], cwd=work)
    git_run(["git", "commit", "-q", "-m", "Initial commit"], cwd=work)
    git_run(["git", "remote", "add", "origin", bare27], cwd=work)
    git_run(["git", "push", "-q", "origin", "master"], cwd=work)

    # Level 28: password existed in an EARLIER commit, then was removed.
    bare28 = "/home/bandit28-git/repo"
    init_bare(bare28)
    work = f"{TMP}/w28"
    git_run(["git", "init", "-q", "-b", "master", work])
    git_write(f"{work}/README.md",
              "Bandit level 28\n================\n\n"
              f"You found me! The password for the next level is:\n\n{git_flag[28]}\n")
    git_run(["git", "add", "README.md"], cwd=work)
    git_run(["git", "commit", "-q", "-m", "Initial commit of README.md"], cwd=work)
    git_write(f"{work}/README.md",
              "Bandit level 28\n================\n\n"
              "Some data sensitive to this repository has been committed here, "
              "please remove it.\n\nFor now, this file is a placeholder.\n")
    git_run(["git", "add", "README.md"], cwd=work)
    git_run(["git", "commit", "-q", "-m", "Fix by removing spurious content, use $EDITOR properly next time"], cwd=work)
    git_run(["git", "remote", "add", "origin", bare28], cwd=work)
    git_run(["git", "push", "-q", "origin", "master"], cwd=work)

    # Level 29: password only exists on a non-default branch (with a decoy).
    bare29 = "/home/bandit29-git/repo"
    init_bare(bare29)
    work = f"{TMP}/w29"
    git_run(["git", "init", "-q", "-b", "master", work])
    git_write(f"{work}/README.md",
              "Bandit level 29\n================\n\nThis is not the branch you are looking for.\n"
              "Maybe check the git branches?\n")
    git_run(["git", "add", "README.md"], cwd=work)
    git_run(["git", "commit", "-q", "-m", "Initial commit"], cwd=work)
    git_run(["git", "checkout", "-q", "-b", "fix-readme-instructions"], cwd=work)
    git_write(f"{work}/README.md",
              "Bandit level 29\n================\n\nNothing here either, sorry. Keep looking.\n")
    git_run(["git", "add", "README.md"], cwd=work)
    git_run(["git", "commit", "-q", "-m", "Nothing yet"], cwd=work)
    git_run(["git", "checkout", "-q", "-b", "dev", "master"], cwd=work)
    git_write(f"{work}/README.md",
              "Bandit level 29\n================\n\n"
              f"You found me! The password for the next level is:\n\n{git_flag[29]}\n")
    git_run(["git", "add", "README.md"], cwd=work)
    git_run(["git", "commit", "-q", "-m", "Add development notes"], cwd=work)
    git_run(["git", "remote", "add", "origin", bare29], cwd=work)
    git_run(["git", "push", "-q", "origin", "master"], cwd=work)
    git_run(["git", "push", "-q", "origin", "fix-readme-instructions"], cwd=work)
    git_run(["git", "push", "-q", "origin", "dev"], cwd=work)

    # Level 30: password only reachable via an annotated tag.
    bare30 = "/home/bandit30-git/repo"
    init_bare(bare30)
    work = f"{TMP}/w30"
    git_run(["git", "init", "-q", "-b", "master", work])
    git_write(f"{work}/README.md",
              "Bandit level 30\n================\n\nCome back when you know more about tags.\n")
    git_run(["git", "add", "README.md"], cwd=work)
    git_run(["git", "commit", "-q", "-m", "Initial commit"], cwd=work)
    git_run(["git", "tag", "-a", "secret", "-m", f"Congratulations, the password is {git_flag[30]}"], cwd=work)
    git_run(["git", "remote", "add", "origin", bare30], cwd=work)
    git_run(["git", "push", "-q", "origin", "master"], cwd=work)
    git_run(["git", "push", "-q", "--tags", "origin"], cwd=work)

    # Level 31: pre-receive hook reveals the password on a correctly-formed push.
    bare31 = "/home/bandit31-git/repo"
    init_bare(bare31)
    work = f"{TMP}/w31"
    git_run(["git", "init", "-q", "-b", "master", work])
    git_write(f"{work}/README.md",
              "Bandit level 31\n================\n\n"
              "This time your task is to push a file to the remote repository.\n\n"
              "Details:\n"
              "    Clone this repository.\n"
              "    Create/edit a file called key.txt and place the content "
              "\"May I come in?\" in it.\n"
              "    Push a file named key.txt to the master branch of this "
              "repository (not any other branch).\n")
    git_run(["git", "add", "README.md"], cwd=work)
    git_run(["git", "commit", "-q", "-m", "Initial commit"], cwd=work)
    git_run(["git", "remote", "add", "origin", bare31], cwd=work)
    git_run(["git", "push", "-q", "origin", "master"], cwd=work)

    hook = (
        "#!/bin/bash\n"
        "while read oldrev newrev refname; do\n"
        '    if [ "$refname" != "refs/heads/master" ]; then\n'
        '        echo "Only pushes to refs/heads/master are evaluated." >&2\n'
        "        continue\n"
        "    fi\n"
        '    content=$(git show "${newrev}:key.txt" 2>/dev/null)\n'
        '    if [ "$content" = "May I come in?" ]; then\n'
        '        echo "" >&2\n'
        '        echo "Well done! Here is your key:" >&2\n'
        f'        echo "{git_flag[31]}" >&2\n'
        '        echo "" >&2\n'
        "    else\n"
        '        echo "Wrong content in key.txt (or key.txt is missing)." >&2\n'
        "    fi\n"
        "done\n"
        "exit 1\n"
    )
    git_write(f"{bare31}/hooks/pre-receive", hook)
    os.chmod(f"{bare31}/hooks/pre-receive", 0o755)

    for n in (27, 28, 29, 30, 31):
        subprocess.run(["chown", "-R", f"bandit{n}-git:bandit{n}-git", f"/home/bandit{n}-git"], check=True)

    subprocess.run(["rm", "-rf", TMP], check=False)

    with open("/etc/shells", "a") as f:
        f.write("/usr/bin/git-shell\n")
PYEOF
else
    echo "WARNING: no LEVEL_SECRETS set -- bandit1-33 will not be playable until content is synced." >&2
fi

for daemon in /opt/bandit-daemons/*.py; do
    [ -e "$daemon" ] || continue
    su banditd -s /bin/bash -c "python3 '$daemon'" &
done

cron

exec /usr/sbin/sshd -D
