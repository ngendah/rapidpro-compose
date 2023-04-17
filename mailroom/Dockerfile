FROM ubuntu:latest

ARG TZ
ARG MAILROOM_REPO
ARG MAILROOM_VERSION
ENV TZ=${TZ:-Africa/Nairobi}
ENV MAILROOM_VERSION=$MAILROOM_VERSION

RUN set -ex \
    && apt-get -y update \
    && apt-get install -y wget tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && addgroup --system mailroom \
    && adduser --system --ingroup mailroom mailroom

USER mailroom
RUN mkdir -p /home/mailroom/app
WORKDIR /home/mailroom
RUN set -ex; \
    wget -qO mailroom.tar.gz "https://github.com/rapidpro/mailroom/releases/download/v${MAILROOM_VERSION}/mailroom_${MAILROOM_VERSION}_linux_amd64.tar.gz" \
    && tar -C ./app -xf mailroom.tar.gz \
    && rm -rf mailroom mailroom.tar.gz
WORKDIR app
COPY startup.sh .
EXPOSE 8090
ENTRYPOINT ["/bin/sh"]
CMD ["-c", "sleep 4000"]
