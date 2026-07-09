#!/bin/bash
set -e

mkdir -p /var/run/mysqld
chown mysql:mysql /var/run/mysqld
mysqld_safe --datadir=/var/lib/mysql --bind-address=127.0.0.1 &

for i in $(seq 1 30); do
    mysqladmin ping --silent && break
    sleep 1
done

# Must be a genuine exec of the apache2 binary AS apache-itk-idle (not
# started as root and setuid()'d down internally) for the file
# capabilities granted via `setcap` at build time to actually apply --
# see the Dockerfile comment next to the `setcap` call.
exec su -s /bin/bash apache-itk-idle -c "exec apache2ctl -D FOREGROUND"
