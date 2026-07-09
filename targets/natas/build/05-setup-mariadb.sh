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

mysqld_safe --datadir=/var/lib/mysql --skip-networking=0 --bind-address=127.0.0.1 &
for i in $(seq 1 30); do
    mysqladmin ping --silent && break
    sleep 1
done

mysql -u root <<'SQL'
CREATE DATABASE IF NOT EXISTS natas14;
USE natas14;
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(64) PRIMARY KEY,
    password VARCHAR(64) NOT NULL
);
REPLACE INTO users (username, password) VALUES ('natas14', 'CHANGEME_NOT_THE_REAL_FLAG_9f31');

CREATE USER IF NOT EXISTS 'natas14'@'127.0.0.1' IDENTIFIED BY 'natas14dbP4ss';
GRANT SELECT ON natas14.users TO 'natas14'@'127.0.0.1';
FLUSH PRIVILEGES;
SQL

mysqladmin -u root shutdown
