FROM ubuntu:20.04

ARG COURIER_REPO
ARG COURIER_VERSION
ARG TZ
ENV TZ=${TZ:-Africa/Nairobi}
ENV COURIER_VERSION=$COURIER_VERSION 

RUN set -ex \
    && apt-get -y update \
    && apt-get install -y wget tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && addgroup --system courier \
    && adduser --system --ingroup courier courier

USER courier
RUN mkdir -p /home/courier/app
WORKDIR /home/courier
RUN set -ex \
    && wget -qO courier.tar.gz "https://github.com/nyaruka/courier/releases/download/v${COURIER_VERSION}/courier_${COURIER_VERSION}_linux_amd64.tar.gz" \ 
    && tar -C ./app -xf courier.tar.gz \
    && rm -rf courier.tar.gz

WORKDIR app
COPY startup.sh .
EXPOSE 8080
ENTRYPOINT ["/bin/sh"]
CMD ["-c", "./startup.sh"]
