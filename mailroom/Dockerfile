FROM ubuntu:latest

ARG TZ
ARG MAILROOM_REPO
ARG MAILROOM_VERSION

ENV TZ=${TZ:-Africa/Nairobi}
ENV MAILROOM_REPO=${MAILROOM_REPO:-nyaruka/mailroom}
ENV MAILROOM_VERSION=${MAILROOM_VERSION:-0.0.201} 

RUN set -ex; \
    apt -y update; \
    apt install -y wget tzdata

RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN set -ex; \
    wget -O mailroom.tar.gz "https://github.com/$MAILROOM_REPO/releases/download/v${MAILROOM_VERSION}/mailroom_${MAILROOM_VERSION}_linux_amd64.tar.gz" \
    && mkdir /mailroom \
    && tar -C /mailroom -xf mailroom.tar.gz \
    && mv /mailroom/mailroom /usr/local/bin/ \
    && mv /mailroom/docs / \
    && rm -rf /mailroom mailroom.tar.gz


COPY startup.sh .

EXPOSE 8090
ENTRYPOINT ["sh", "-c", "./startup.sh"]
