FROM ubuntu:latest

ARG TZ
ARG MAILROOM_REPO
ARG MAILROOM_VERSION

ENV TZ=${TZ:-Africa/Nairobi}
ENV MAILROOM_VERSION=$MAILROOM_VERSION

RUN set -ex \
    && apt-get -y update \
    && apt-get install -y wget tzdata

RUN cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

RUN set -ex; \
    wget -qO mailroom.tar.gz "https://github.com/nyaruka/mailroom/releases/download/v${MAILROOM_VERSION}/mailroom_${MAILROOM_VERSION}_linux_amd64.tar.gz" \
    && mkdir /mailroom \
    && tar -C /mailroom -xf mailroom.tar.gz \
    && mv /mailroom/mailroom /usr/local/bin/ \
    && mv /mailroom/docs / \
    && rm -rf /mailroom mailroom.tar.gz

COPY startup.sh .

EXPOSE 8090
ENTRYPOINT ["sh", "-c", "./startup.sh"]
