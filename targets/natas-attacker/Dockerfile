# Natas-specific attacker workstation. The generic CEI Kali/noVNC image
# intentionally stays small, but Natas levels 8+ require byte/encoding
# utilities that are not present there.
#
# Release/event builds should pin the base image for reproducibility by
# passing --build-arg BASE_IMAGE=ghcr.io/stoptalkingishh/cei-labs-engine/ctf-kali-novnc@sha256:<digest>
# (the floating :latest default is for development only).
ARG BASE_IMAGE=ghcr.io/stoptalkingishh/cei-labs-engine/ctf-kali-novnc:latest
FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       xxd \
       bsdextrautils \
       jq \
       python3 \
       python3-requests \
       file \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# A durable, offline reminder discoverable from any terminal.
RUN printf '%s\n' \
    '#!/bin/sh' \
    'cat <<'"'"'EOF'"'"'' \
    'Natas workstation tools:' \
    '  curl -u USER:PASSWORD URL       authenticated HTTP request' \
    '  xxd -r -p                      hexadecimal text -> raw bytes' \
    '  rev                            reverse each input line' \
    '  base64 -d                      Base64 text -> decoded bytes' \
    '  python3                        scripting/XOR analysis' \
    '  file                           inspect uploaded file types' \
    'EOF' \
    > /usr/local/bin/natas-help \
    && chmod 755 /usr/local/bin/natas-help

# The base image's noVNC web UI on 6080 is the workstation's only player
# access path (see docs/self-hosted-wargames-blueprint.md), so that's
# what "healthy" means here. Probe the listener with bash's /dev/tcp --
# a bare TCP connect is enough (any listener means the noVNC proxy is
# up) and needs nothing beyond bash, which Kali always has.
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD bash -c 'exec 3<>/dev/tcp/127.0.0.1/6080' || exit 1
