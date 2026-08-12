ARG BASE_IMAGE=ghcr.io/stoptalkingishh/cei-labs-engine/target-base-linux:latest
FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 openssl iproute2 procps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY runtime.py /opt/sentinel/runtime.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod 700 /opt/sentinel/runtime.py /entrypoint.sh \
    && for number in 0 1 2 3 4 5; do useradd -m -s /bin/bash --no-log-init "sentinel${number}"; chmod 750 "/home/sentinel${number}"; done \
    && echo 'sentinel0:sentinel0' | chpasswd \
    && openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
        -keyout /tmp/sentinel-service.key -out /home/sentinel4/service.pem \
        -subj '/CN=ops.northstar.training' \
    && rm -f /tmp/sentinel-service.key \
    && chown sentinel4:sentinel4 /home/sentinel4/service.pem \
    && chmod 400 /home/sentinel4/service.pem \
    && mkdir -p /var/lib/sentinel \
    && chown root:root /var/lib/sentinel \
    && chmod 700 /var/lib/sentinel

EXPOSE 22
CMD ["/entrypoint.sh"]
