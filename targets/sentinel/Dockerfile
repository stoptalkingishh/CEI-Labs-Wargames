ARG BASE_IMAGE=ghcr.io/stoptalkingishh/cei-labs-engine/target-base-linux:latest
FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 openssl iproute2 procps gcc libc6-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY runtime.py /opt/sentinel/runtime.py
COPY answer_service.py /opt/sentinel/answer_service.py
COPY submit.c /opt/sentinel/submit.c
COPY certs /opt/sentinel/certs
COPY fixtures /opt/sentinel/fixtures
COPY entrypoint.sh /entrypoint.sh
RUN gcc -O2 -Wall -Wextra -Werror -o /usr/local/bin/sentinel-submit /opt/sentinel/submit.c \
    && chown root:root /usr/local/bin/sentinel-submit /opt/sentinel/answer_service.py \
    && chmod 4755 /usr/local/bin/sentinel-submit \
    && chown -R root:root /opt/sentinel \
    && chmod 700 /opt/sentinel /opt/sentinel/certs /opt/sentinel/fixtures /opt/sentinel/runtime.py /opt/sentinel/answer_service.py /entrypoint.sh \
    && chmod 600 /opt/sentinel/certs/service.key \
    && chmod 644 /opt/sentinel/certs/training-ca.pem /opt/sentinel/certs/training-ca.crl /opt/sentinel/certs/service.pem \
    && for number in 0 1 2 3 4 5 22 23 24 25 26 27; do useradd -m -s /bin/bash --no-log-init "sentinel${number}"; chmod 750 "/home/sentinel${number}"; ln -s "/srv/sentinel-evidence/sentinel${number}" "/home/sentinel${number}/evidence"; chown -h root:root "/home/sentinel${number}/evidence"; done \
    && echo 'sentinel0:sentinel0' | chpasswd \
    && mkdir -p /var/lib/sentinel \
    && chown root:root /var/lib/sentinel \
    && chmod 700 /var/lib/sentinel \
    && mkdir -p /srv/sentinel-evidence \
    && chown root:root /srv/sentinel-evidence \
    && chmod 755 /srv/sentinel-evidence \
    && for number in 0 1 2 3 4 5 22 23 24 25 26 27; do mkdir "/srv/sentinel-evidence/sentinel${number}"; chown root:root "/srv/sentinel-evidence/sentinel${number}"; chmod 755 "/srv/sentinel-evidence/sentinel${number}"; done

EXPOSE 22
CMD ["/entrypoint.sh"]
