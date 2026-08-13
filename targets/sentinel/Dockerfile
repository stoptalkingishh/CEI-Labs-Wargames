ARG BASE_IMAGE=ghcr.io/stoptalkingishh/cei-labs-engine/target-base-linux:latest
FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 openssl iproute2 procps gcc libc6-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY runtime.py /opt/sentinel/runtime.py
COPY answer_service.py /opt/sentinel/answer_service.py
COPY submit.c /opt/sentinel/submit.c
COPY certs /opt/sentinel/certs
COPY entrypoint.sh /entrypoint.sh
RUN gcc -O2 -Wall -Wextra -Werror -o /usr/local/bin/sentinel-submit /opt/sentinel/submit.c \
    && chown root:root /usr/local/bin/sentinel-submit /opt/sentinel/answer_service.py \
    && chmod 4755 /usr/local/bin/sentinel-submit \
    && chmod 700 /opt/sentinel/runtime.py /opt/sentinel/answer_service.py /entrypoint.sh \
    && for number in 0 1 2 3 4 5; do useradd -m -s /bin/bash --no-log-init "sentinel${number}"; chmod 750 "/home/sentinel${number}"; done \
    && echo 'sentinel0:sentinel0' | chpasswd \
    && mkdir -p /var/lib/sentinel \
    && chown root:root /var/lib/sentinel \
    && chmod 700 /var/lib/sentinel

EXPOSE 22
CMD ["/entrypoint.sh"]
