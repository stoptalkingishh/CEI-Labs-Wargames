#!/bin/bash
set -e

# Per-team secrets for levels 1-14 (webpass files + htpasswd hashes) and
# the level-14 final flag, generated fresh by cei-labs-engine's
# orchestrator at container START from $LEVEL_SECRETS (a JSON blob) --
# not identical hardcoded values baked into every build (see
# docs/security-audit-status.md). natas0's password stays the real,
# public "natas0" (OverTheWire's well-known bootstrap credential, not a
# secret). If $LEVEL_SECRETS is missing a key (e.g. CTFd content hasn't
# been synced with the per_team_dynamic flags yet), that level's webpass/
# htpasswd files are simply left as the invalid build-time placeholder
# (locked out -- a safe failure mode, not a shared-credential one), and
# any content-page placeholder text stays literally visible rather than
# silently falling back to a shared value.
if [ -n "${LEVEL_SECRETS:-}" ]; then
    python3 - <<'PYEOF'
import json
import os
import subprocess

secrets = json.loads(os.environ.get("LEVEL_SECRETS", "{}"))

for n in range(1, 15):
    key = f"natas{n}"
    value = secrets.get(key)
    if not value:
        continue
    prev = n - 1

    webpass_path = f"/etc/natas_webpass/natas{n}"
    with open(webpass_path, "w") as f:
        f.write(value)
    subprocess.run(["chown", f"natas{n}:natas{prev}", webpass_path], check=True)
    os.chmod(webpass_path, 0o640)

    htpasswd_path = f"/etc/apache2/natas-htpasswd/natas{n}"
    subprocess.run(["htpasswd", "-bBc", htpasswd_path, key, value], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["chown", f"{key}:{key}", htpasswd_path], check=True)
    os.chmod(htpasswd_path, 0o600)

# Content pages that embed the NEXT level's password as visible text/
# HTML content with no "view source" feature on the same page -- the
# intended discovery mechanism for these levels IS reading the page
# content, so a plain placeholder substitution is safe (natas2/3/7/9/10/
# 12/13 instead read the webpass file directly through their own
# vulnerability, so they need no content-file changes of any kind).
CONTENT_SUBS = {
    "/var/www/natas/natas0/index.php": ("__NATAS1_SECRET__", "natas1"),
    "/var/www/natas/natas1/index.php": ("__NATAS2_SECRET__", "natas2"),
    "/var/www/natas/natas2/files/users.txt": ("__NATAS3_SECRET__", "natas3"),
    "/var/www/natas/natas3/s3cr3t/users.txt": ("__NATAS4_SECRET__", "natas4"),
    "/var/www/natas/natas4/index.php": ("__NATAS5_SECRET__", "natas5"),
    "/var/www/natas/natas5/index.php": ("__NATAS6_SECRET__", "natas6"),
}
for path, (placeholder, key) in CONTENT_SUBS.items():
    value = secrets.get(key)
    if not value or not os.path.exists(path):
        continue
    with open(path, "r") as f:
        content = f.read()
    with open(path, "w") as f:
        f.write(content.replace(placeholder, value))

# Levels 6, 8, 11, 14 each have their own "?source" highlight_file()
# view-source feature -- a plain inline placeholder substitution would
# still be readable via that feature regardless of whether the level's
# own puzzle is solved, since highlight_file() dumps the raw file text
# with no awareness of runtime state. Writing the per-team value into a
# SEPARATE file that the main page require()s keeps it out of what
# highlight_file(__FILE__) ever shows.
NEXT_PASSWORD_FILES = {
    "/var/www/natas/natas6/next_password.php": ("natas6", "natas7", "next_password"),
    "/var/www/natas/natas8/next_password.php": ("natas8", "natas9", "next_password"),
    "/var/www/natas/natas11/next_password.php": ("natas11", "natas12", "next_password"),
    "/var/www/natas/natas14/next_password.php": ("natas14", "natas14final", "final_flag"),
}
for path, (owner, key, var_name) in NEXT_PASSWORD_FILES.items():
    value = secrets.get(key)
    if not value:
        continue
    php_string = value.replace("\\", "\\\\").replace("'", "\\'")
    with open(path, "w") as f:
        f.write(f"<?php ${var_name} = '{php_string}';\n")
    subprocess.run(["chown", f"{owner}:{owner}", path], check=True)
    os.chmod(path, 0o600)
PYEOF
else
    echo "WARNING: no LEVEL_SECRETS set -- natas1-14 will not be playable until content is synced." >&2
fi

mkdir -p /var/run/mysqld
chown mysql:mysql /var/run/mysqld
mysqld_safe --datadir=/var/lib/mysql --bind-address=127.0.0.1 &

for i in $(seq 1 30); do
    mysqladmin ping --silent && break
    sleep 1
done

# Security: plain `su` (no -l/-) on Debian preserves the calling
# process's ENTIRE environment for the target process, including
# $LEVEL_SECRETS -- the JSON blob holding every level's password AND the
# final flag for this team, only ever meant to be read by the python3
# heredoc above. Apache/PHP have no legitimate need for it, but every
# apache2/PHP worker forked from this exec'd process would otherwise
# inherit it verbatim, making it readable via getenv()/$_ENV, PHP's
# phpinfo(), or the raw /proc/<pid>/environ file of any worker. Several
# Natas levels are INTENTIONALLY vulnerable to arbitrary file read/
# inclusion or code execution as their whole teaching point (e.g.
# natas7's unsanitized `include($_GET['page'])`, natas12/13's upload
# RCE) -- solving any one of those was meant to leak only that level's
# own /etc/natas_webpass/natasN file (see 02-set-webpasswords.sh's
# narrow per-level ownership/chmod), not every other level's password
# and the final flag in one shot via /proc/self/environ. Explicitly
# scrubbing just this one variable (not `su -l`, which would also reset
# PATH to a non-root ENV_PATH lacking /usr/sbin and break `apache2ctl`)
# closes that off while leaving everything else Apache legitimately
# needs (PATH, etc.) untouched.
unset LEVEL_SECRETS

# Must be a genuine exec of the apache2 binary AS apache-itk-idle (not
# started as root and setuid()'d down internally) for the file
# capabilities granted via `setcap` at build time to actually apply --
# see the Dockerfile comment next to the `setcap` call.
exec su -s /bin/bash apache-itk-idle -c "exec apache2ctl -D FOREGROUND"
