# CEI-Labs-Wargames/targets/natas
# Self-hosted recreation of OverTheWire's Natas wargame (levels 0-14),
# a single LAMP box reachable ONLY from its own team's attacker over the
# range's private network (target-attacker instance type -- no
# externally published port at all, not even SSH). See
# CEI-Labs-Wargames/docs/self-hosted-wargames-blueprint.md Phase 4.
#
# PHP 5.6 is not a placeholder choice: level 14's SQLi lesson needs the
# legacy mysql_connect()/mysql_query() extension, removed entirely in
# PHP 7. Installed via the still-maintained sury.org legacy-PHP APT repo
# on top of the same base-linux target image Bandit/Krypton use (itself
# debian:12-slim), keeping one base-OS family project-wide. This image
# never starts the base image's sshd -- target-attacker instances have
# no inbound access at all except from their own range's attacker.
ARG BASE_IMAGE=ghcr.io/stoptalkingishh/cei-labs-engine/target-base-linux:latest
FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg \
    lsb-release \
    python3 \
    python3-minimal \
    && curl -fsSL https://packages.sury.org/php/apt.gpg -o /etc/apt/trusted.gpg.d/sury-php.gpg \
    && echo "deb https://packages.sury.org/php/ bookworm main" > /etc/apt/sources.list.d/sury-php.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       apache2 \
       libapache2-mpm-itk \
       apache2-utils \
       php5.6 \
       libapache2-mod-php5.6 \
       php5.6-mysql \
       php5.6-exif \
       mariadb-server \
       openssl \
       libcap2-bin \
    && apt-get purge -y gnupg lsb-release \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# mpm_itk.load's own packaging comment ("# Depends: mpm_prefork") is
# literal -- itk's .so shares code with prefork's and genuinely needs it
# loaded too; removing prefork produces "No MPM loaded", confirmed by
# testing. Just confirm itk itself is present.
RUN apache2ctl -M 2>&1 | grep -q mpm_itk_module || (echo "mpm_itk not active" && apache2ctl -M && exit 1)

# MPM-ITK's idle worker pool starts as the GLOBAL default User/Group
# (www-data via envvars.conf by default) and only setuid/setgid's to a
# vhost's AssignUserID identity once it's actually handling a request for
# that vhost -- but a plain www-data process has no capability left to
# switch to anything else (confirmed by testing: setgid() from a fresh
# root process works fine, but idle apache2 workers were already uid=33
# at container startup, before any request, and their per-vhost setgid()
# attempts failed with EPERM).
#
# Least-privilege fix: a dedicated, otherwise-unprivileged system user
# for the idle pool, with the setuid/setgid capability granted narrowly
# to the apache2 BINARY itself (Linux file capabilities) rather than
# running any process as root. The master must actually be EXEC'd as
# this user (not started as root then setuid()'d down internally) for
# the file capability to apply -- see entrypoint.sh.
RUN useradd -r -M -s /usr/sbin/nologin apache-itk-idle \
    && setcap 'cap_setuid,cap_setgid+eip' /usr/sbin/apache2 \
    && sed -i \
       -e 's/^export APACHE_RUN_USER=.*/export APACHE_RUN_USER=apache-itk-idle/' \
       -e 's/^export APACHE_RUN_GROUP=.*/export APACHE_RUN_GROUP=apache-itk-idle/' \
       /etc/apache2/envvars \
    && mkdir -p /var/run/apache2 /var/lock/apache2 \
    && chown -R apache-itk-idle:apache-itk-idle /var/run/apache2 /var/lock/apache2 /var/log/apache2

COPY build/ /opt/build/
RUN chmod +x /opt/build/*.sh /opt/build/*.py

# Users, per-level webpass files, MariaDB schema/users, Apache vhosts,
# and PHP content -- see each script's own header comment for what it
# owns.
RUN /opt/build/01-create-users.sh \
    && /opt/build/02-set-webpasswords.sh \
    && python3 /opt/build/03-generate-vhosts.py

COPY content/ /var/www/natas/
RUN /opt/build/04-fix-content-ownership.sh \
    && /opt/build/05-setup-mariadb.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Deliberately NO EXPOSE of any external-facing port declaration beyond
# what Apache itself binds to internally -- this image is only ever
# reached over the range's private network, never published to the host.
EXPOSE 8000-8014

CMD ["/entrypoint.sh"]
