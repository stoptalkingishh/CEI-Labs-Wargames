# CEI-Labs-Wargames/targets/krypton
# Self-hosted recreation of OverTheWire's Krypton wargame (levels 0-6),
# one persistent SSH machine per team, same "one box, many levels"
# design as targets/bandit. See
# CEI-Labs-Wargames/docs/self-hosted-wargames-blueprint.md Phase 3.
#
# Multi-stage: levels 2 and 6 ship compiled `encrypt` binaries (so the
# shift/keystream isn't just readable in a script); the compiler itself
# has no business in the final image.
FROM debian:12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*
COPY src/caesar_encrypt.c src/lfsr_encrypt.c /tmp/
RUN gcc -O2 -o /tmp/caesar_encrypt /tmp/caesar_encrypt.c \
    && gcc -O2 -o /tmp/lfsr_encrypt /tmp/lfsr_encrypt.c

FROM ghcr.io/local-test/cei-labs-engine/target-base-linux:dev

ARG DEBIAN_FRONTEND=noninteractive

# Crypto tooling, with alternatives installed side by side so players can
# use whichever they're already comfortable with: python3 for scripted
# analysis, openssl CLI, both xxd and hexdump, base64/base32, tr for
# classic Caesar/ROT13 one-liners.
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-minimal \
    openssl \
    xxd \
    bsdextrautils \
    coreutils \
    binutils \
    vim \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY build/ /opt/build/
RUN chmod +x /opt/build/*.sh /opt/build/*.py \
    && /opt/build/01-create-users.sh \
    && /opt/build/02-set-passwords.sh \
    && python3 /opt/build/03-setup-content.py

# Level 2 and level 6 each get their own copy of the relevant compiled
# binary, matching the per-level "the tool lives next to the puzzle it
# solves" layout the descriptions already reference.
COPY --from=builder /tmp/caesar_encrypt /krypton/krypton2/encrypt
COPY --from=builder /tmp/lfsr_encrypt /krypton/krypton6/encrypt
# Level 2 and level 6's keyfile/keystream/ciphertext/README are
# deliberately NOT generated here -- they're per-team secrets, generated
# fresh by entrypoint.sh at container START from $LEVEL_SECRETS (see
# docs/security-audit-status.md). Only the encrypt binaries themselves
# are build-time content.
RUN mkdir -p /krypton/krypton2 /krypton/krypton6 \
    && chmod +x /krypton/krypton2/encrypt /krypton/krypton6/encrypt \
    && rm -rf /opt/build

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22

CMD ["/entrypoint.sh"]
