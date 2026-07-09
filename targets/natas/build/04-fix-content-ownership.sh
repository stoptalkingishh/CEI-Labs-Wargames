#!/bin/bash
# Content under /var/www/natas is world-readable by default (root-owned,
# 644/755) -- correct for every level except the two file-upload levels
# (12, 13), whose upload destinations must actually be writable BY that
# level's own AssignUserID identity. 755 (not a stricter 770) is
# deliberate: Apache's own .htaccess-existence check on this directory
# happens outside the request's already-switched-to-natasN identity in a
# way that needs at least traverse+read on the dir regardless of who's
# asking (confirmed by testing -- 770 produced "unable to check htaccess
# file" 403s even for the owning identity's own later GET requests); only
# WRITE needs to stay narrowly scoped to that level's own user, which the
# owner bit alone already guarantees.
set -e

chown -R root:root /var/www/natas
find /var/www/natas -type d -exec chmod 755 {} \;
find /var/www/natas -type f -exec chmod 644 {} \;

for n in 12 13; do
    upload_dir="/var/www/natas/natas${n}/uploads"
    mkdir -p "$upload_dir"
    chown "natas${n}:natas${n}" "$upload_dir"
    chmod 755 "$upload_dir"
done
