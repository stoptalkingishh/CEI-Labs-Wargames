# Natas-specific attacker workstation. The generic CEI Kali/noVNC image
# intentionally stays small, but Natas levels 8+ require byte/encoding
# utilities that are not present there.
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
