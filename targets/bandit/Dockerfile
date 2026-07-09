# CEI-Labs-Wargames/targets/bandit
# Self-hosted recreation of OverTheWire's Bandit wargame (levels 0-33),
# one persistent SSH machine per team, matching the real game's actual
# design (all 34 levels live on ONE box, progressed by escalating from
# bandit(N) to bandit(N+1) using a password discovered by exploiting the
# current level). See CEI-Labs-Wargames/docs/self-hosted-wargames-blueprint.md
# Phase 2 for the full per-level design rationale and flag-provenance notes.
#
# Built FROM cei-labs-engine's operator/targets/base-linux, per that
# image's own documented extension contract.
FROM ghcr.io/local-test/cei-labs-engine/target-base-linux:dev

ARG DEBIAN_FRONTEND=noninteractive

# Level-solving toolset -- deliberately includes multiple alternatives per
# task (two editors, three netcat variants, two Pythons where relevant) so
# players can use whichever they're already comfortable with, matching the
# blueprint's "multiple tools" requirement. Driven by what the 34 lessons
# actually need: find/grep/awk/sed/sort/diff/file/strings for the file-
# puzzle levels, xxd for the hexdump level, tar/gzip/bzip2/xz for the
# compression level, git for the git-repo levels, cron for the cron
# levels, openssh-client for the level-13 key hop.
RUN apt-get update && apt-get install -y --no-install-recommends \
    findutils \
    grep \
    gawk \
    sed \
    coreutils \
    diffutils \
    file \
    binutils \
    xxd \
    tar \
    gzip \
    bzip2 \
    xz-utils \
    git \
    cron \
    openssh-client \
    netcat-openbsd \
    ncat \
    socat \
    openssl \
    python3 \
    python3-minimal \
    vim \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Unprivileged account that runs the port-listener daemons (level 14+) --
# never root, never a player account, so a compromised daemon can't hand a
# player root or another level's account for free.
RUN useradd -r -m -s /usr/sbin/nologin banditd

COPY build/ /opt/build/
RUN chmod +x /opt/build/*.sh /opt/build/*.py \
    && /opt/build/01-create-users.sh \
    && /opt/build/02-set-passwords.sh \
    && python3 /opt/build/03-setup-levels-00-12.py \
    && /opt/build/04-setup-level-13.sh \
    && /opt/build/05-setup-tls.sh \
    && python3 /opt/build/06-setup-levels-17-18.py \
    && rm -rf /opt/build

COPY daemons/ /opt/bandit-daemons/
RUN chown -R banditd:banditd /opt/bandit-daemons \
    && chmod 500 /opt/bandit-daemons/*.py

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 22 for SSH (all players); 30000+ range for the port-submission levels
# (14 onward) -- these are internal-network-only in production (the
# orchestrator's single-target model publishes only port 22 externally;
# the 3000x ports are reachable from inside the box itself, which is all
# these levels need since players interact with them from their own SSH
# session on this same host).
EXPOSE 22

CMD ["/entrypoint.sh"]
