#!/usr/bin/env python3
"""Bandit levels 27-31: five git-shell service accounts (bandit27-git ..
bandit31-git), each logged into with the SAME password as the
correspondingly-numbered bandit(N) player account (that's the actual
lesson text: "using the SSH password you already have"), each serving one
bare repo whose git history/branches/tags/hooks hide the next level's
password. Matches the real game's five-lesson git arc:
  27 -> plain file at HEAD
  28 -> file existed in an older commit, since removed
  29 -> file exists only on a non-default branch
  30 -> file exists only via a tag
  31 -> password is revealed by a pre-receive hook on a successful push,
        not by anything clone-able
"""
import os
import subprocess

# bandit(N)'s own password -- used both as bandit(N)-git's login password
# (the git-shell account) and to double check we're wiring the chain up
# the same way 02-set-passwords.sh already did.
PW = {
    27: "3ba3118a22e93127a4ed485be72ef5ea",
    28: "0ef186ac70e04ea33b4c1853d2526fa2",
    29: "bbc96594b4e001778eee9975372716b2",
    30: "5b90576ed34ce8c56ad62351ab66e47c",
    31: "47e603bb428404d265f59c42920d81e5",
}
# What each level's git puzzle reveals -- bandit(N)'s own flag, i.e.
# bandit(N+1)'s password.
FLAG = {
    27: "0ef186ac70e04ea33b4c1853d2526fa2",  # -> bandit28's password
    28: "bbc96594b4e001778eee9975372716b2",  # -> bandit29's password
    29: "5b90576ed34ce8c56ad62351ab66e47c",  # -> bandit30's password
    30: "47e603bb428404d265f59c42920d81e5",  # -> bandit31's password
    31: "56a9bf19c63d650ce78e6ec0354ee45e",  # -> bandit32's password
}

TMP = "/opt/build/tmp-git"
GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="CEI Labs", GIT_AUTHOR_EMAIL="build@cei-labs.local",
               GIT_COMMITTER_NAME="CEI Labs", GIT_COMMITTER_EMAIL="build@cei-labs.local")


def run(cmd, cwd=None, check=True):
    subprocess.run(cmd, cwd=cwd, env=GIT_ENV, check=check,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def write(path, content):
    with open(path, "w", newline="\n") as f:
        f.write(content)


def create_git_shell_account(n):
    user = f"bandit{n}-git"
    subprocess.run(["useradd", "-m", "-s", "/usr/bin/git-shell", "--no-log-init", user], check=True)
    subprocess.run(["chpasswd"], input=f"{user}:{PW[n]}\n".encode(), check=True)


def init_bare(path, owner):
    os.makedirs(path, exist_ok=True)
    run(["git", "init", "-q", "--bare", path])


def chown_r(path, owner):
    subprocess.run(["chown", "-R", f"{owner}:{owner}", path], check=True)


for n in (27, 28, 29, 30, 31):
    create_git_shell_account(n)

os.makedirs(TMP, exist_ok=True)

# ---- Level 27: password sitting in a file at HEAD, nothing more to it. ----
bare27 = "/home/bandit27-git/repo"
init_bare(bare27, "bandit27-git")
work = f"{TMP}/w27"
run(["git", "init", "-q", "-b", "master", work])
write(f"{work}/README.md",
      "Bandit level 27\n================\n\n"
      f"You found me! The password for the next level is:\n\n{FLAG[27]}\n")
run(["git", "add", "README.md"], cwd=work)
run(["git", "commit", "-q", "-m", "Initial commit"], cwd=work)
run(["git", "remote", "add", "origin", bare27], cwd=work)
run(["git", "push", "-q", "origin", "master"], cwd=work)

# ---- Level 28: password existed in an EARLIER commit, then was removed.
# Player has to `git log -p` (or `git show <sha>`), not just read HEAD. ----
bare28 = "/home/bandit28-git/repo"
init_bare(bare28, "bandit28-git")
work = f"{TMP}/w28"
run(["git", "init", "-q", "-b", "master", work])
write(f"{work}/README.md",
      "Bandit level 28\n================\n\n"
      f"You found me! The password for the next level is:\n\n{FLAG[28]}\n")
run(["git", "add", "README.md"], cwd=work)
run(["git", "commit", "-q", "-m", "Initial commit of README.md"], cwd=work)
write(f"{work}/README.md",
      "Bandit level 28\n================\n\n"
      "Some data sensitive to this repository has been committed here, "
      "please remove it.\n\nFor now, this file is a placeholder.\n")
run(["git", "add", "README.md"], cwd=work)
run(["git", "commit", "-q", "-m", "Fix by removing spurious content, use $EDITOR properly next time"], cwd=work)
run(["git", "remote", "add", "origin", bare28], cwd=work)
run(["git", "push", "-q", "origin", "master"], cwd=work)

# ---- Level 29: password only exists on a non-default branch. A decoy
# branch is included so "just checkout the other branch" isn't a
# one-branch-only guess. ----------------------------------------------------
bare29 = "/home/bandit29-git/repo"
init_bare(bare29, "bandit29-git")
work = f"{TMP}/w29"
run(["git", "init", "-q", "-b", "master", work])
write(f"{work}/README.md",
      "Bandit level 29\n================\n\nThis is not the branch you are looking for.\n"
      "Maybe check the git branches?\n")
run(["git", "add", "README.md"], cwd=work)
run(["git", "commit", "-q", "-m", "Initial commit"], cwd=work)
run(["git", "checkout", "-q", "-b", "fix-readme-instructions"], cwd=work)
write(f"{work}/README.md",
      "Bandit level 29\n================\n\nNothing here either, sorry. Keep looking.\n")
run(["git", "add", "README.md"], cwd=work)
run(["git", "commit", "-q", "-m", "Nothing yet"], cwd=work)
run(["git", "checkout", "-q", "-b", "dev", "master"], cwd=work)
write(f"{work}/README.md",
      "Bandit level 29\n================\n\n"
      f"You found me! The password for the next level is:\n\n{FLAG[29]}\n")
run(["git", "add", "README.md"], cwd=work)
run(["git", "commit", "-q", "-m", "Add development notes"], cwd=work)
run(["git", "remote", "add", "origin", bare29], cwd=work)
run(["git", "push", "-q", "origin", "master"], cwd=work)
run(["git", "push", "-q", "origin", "fix-readme-instructions"], cwd=work)
run(["git", "push", "-q", "origin", "dev"], cwd=work)

# ---- Level 30: password only reachable via an annotated tag -- not on
# any branch tip. ------------------------------------------------------------
bare30 = "/home/bandit30-git/repo"
init_bare(bare30, "bandit30-git")
work = f"{TMP}/w30"
run(["git", "init", "-q", "-b", "master", work])
write(f"{work}/README.md",
      "Bandit level 30\n================\n\nCome back when you know more about tags.\n")
run(["git", "add", "README.md"], cwd=work)
run(["git", "commit", "-q", "-m", "Initial commit"], cwd=work)
run(["git", "tag", "-a", "secret", "-m", f"Congratulations, the password is {FLAG[30]}"], cwd=work)
run(["git", "remote", "add", "origin", bare30], cwd=work)
run(["git", "push", "-q", "origin", "master"], cwd=work)
run(["git", "push", "-q", "--tags", "origin"], cwd=work)

# ---- Level 31: nothing to clone-and-read at all. The bare repo has a
# pre-receive hook that only fires on an actual push, inspects the
# incoming tree for a correctly-named-and-worded key.txt on master, and
# prints the password to the client via stderr (always rejecting the push
# afterwards, matching the real "you only get one shot" framing --
# rejecting is what lets the hook run again if a player wants to retry). --
bare31 = "/home/bandit31-git/repo"
init_bare(bare31, "bandit31-git")
work = f"{TMP}/w31"
run(["git", "init", "-q", "-b", "master", work])
write(f"{work}/README.md",
      "Bandit level 31\n================\n\n"
      "This time your task is to push a file to the remote repository.\n\n"
      "Details:\n"
      "    Clone this repository.\n"
      "    Create/edit a file called key.txt and place the content "
      "\"May I come in?\" in it.\n"
      "    Push a file named key.txt to the master branch of this "
      "repository (not any other branch).\n")
run(["git", "add", "README.md"], cwd=work)
run(["git", "commit", "-q", "-m", "Initial commit"], cwd=work)
run(["git", "remote", "add", "origin", bare31], cwd=work)
run(["git", "push", "-q", "origin", "master"], cwd=work)

hook = (
    "#!/bin/bash\n"
    "# Fires on every push to this repo. Inspects the NEW tree for a\n"
    "# correctly-worded key.txt on master; prints the next password to\n"
    "# the pushing client via stderr either way lets them see the\n"
    "# outcome, then always rejects so the working tree here never\n"
    "# actually changes and a player can retry.\n"
    "while read oldrev newrev refname; do\n"
    '    if [ "$refname" != "refs/heads/master" ]; then\n'
    '        echo "Only pushes to refs/heads/master are evaluated." >&2\n'
    "        continue\n"
    "    fi\n"
    '    content=$(git show "${newrev}:key.txt" 2>/dev/null)\n'
    '    if [ "$content" = "May I come in?" ]; then\n'
    '        echo "" >&2\n'
    '        echo "Well done! Here is your key:" >&2\n'
    f'        echo "{FLAG[31]}" >&2\n'
    '        echo "" >&2\n'
    "    else\n"
    '        echo "Wrong content in key.txt (or key.txt is missing)." >&2\n'
    "    fi\n"
    "done\n"
    "exit 1\n"
)
write(f"{bare31}/hooks/pre-receive", hook)
os.chmod(f"{bare31}/hooks/pre-receive", 0o755)

for n in (27, 28, 29, 30, 31):
    chown_r(f"/home/bandit{n}-git", f"bandit{n}-git")

subprocess.run(["rm", "-rf", TMP], check=False)

with open("/etc/shells", "a") as f:
    f.write("/usr/bin/git-shell\n")

print("Levels 27-31 git-shell accounts and repos created.")
