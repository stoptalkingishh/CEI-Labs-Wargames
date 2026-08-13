#!/bin/bash
# Level 14's SQLi lesson needs a real database: a `natas14` schema with a
# `users` table (one decoy row -- the actual solve is bypassing the
# WHERE clause via injection, not learning this password) and a
# low-privilege `natas14` DB user who can only SELECT from that one
# table, matching the file-level privilege boundary every other level
# already uses.
set -e

mkdir -p /var/run/mysqld
chown mysql:mysql /var/run/mysqld

mariadb-install-db --user=mysql --datadir=/var/lib/mysql >/dev/null

# Only level 14 can traverse this directory and read its database settings.
# Upload RCE at levels 12/13 therefore cannot reuse the application account.
db_password=$(openssl rand -hex 32)
install -d -o root -g natas14 -m 710 /etc/cei-labs/natas-db
printf "<?php\n\$natas14_db_host = '127.0.0.1';\n\$natas14_db_user = 'natas14';\n\$natas14_db_password = '%s';\n" "$db_password" > /etc/cei-labs/natas-db/natas14.php
chown natas14:natas14 /etc/cei-labs/natas-db/natas14.php
chmod 600 /etc/cei-labs/natas-db/natas14.php

mysqld_safe --datadir=/var/lib/mysql --skip-networking=0 --bind-address=127.0.0.1 &
for i in $(seq 1 30); do
    mysqladmin ping --silent && break
    sleep 1
done

mysql -u root <<SQL
CREATE DATABASE IF NOT EXISTS natas14;
USE natas14;
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(64) PRIMARY KEY,
    password VARCHAR(64) NOT NULL
);
REPLACE INTO users (username, password) VALUES ('natas14', 'CHANGEME_NOT_THE_REAL_FLAG_9f31');

CREATE USER IF NOT EXISTS 'natas14'@'127.0.0.1' IDENTIFIED BY '${db_password}';
GRANT SELECT ON natas14.users TO 'natas14'@'127.0.0.1';
FLUSH PRIVILEGES;
SQL

mysqladmin -u root shutdown
