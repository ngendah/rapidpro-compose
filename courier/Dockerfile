FROM ubuntu:latest

ARG COURIER_REPO
ARG COURIER_VERSION

ARG TZ
ENV TZ=${TZ:-Africa/Nairobi}
ENV COURIER_VERSION=$COURIER_VERSION 

RUN set -ex \
    && apt-get -y update \
    && apt-get install -y wget tzdata

RUN cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

RUN set -ex \
    && wget -qO courier.tar.gz "https://github.com/nyaruka/courier/releases/download/v${COURIER_VERSION}/courier_${COURIER_VERSION}_linux_amd64.tar.gz" \
    && mkdir /courier \
    && tar -C /courier -xf courier.tar.gz \
    && mv /courier/courier /usr/local/bin/ \
    && rm -rf /courier courier.tar.gz

COPY startup.sh .

EXPOSE 8080
ENTRYPOINT ["sh", "-c", "./startup.sh"]
