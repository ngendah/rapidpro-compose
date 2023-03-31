FROM nginx:alpine

ARG TZ
ARG CERT_ORG_NAME
ARG CERT_COMMON_NAME

ENV TZ=${TZ:-Africa/Nairobi}

RUN apk add --no-cache --virtual .deps openssl tzdata
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN set -ex \
    && mkdir -p /etc/ssl \
    && cd /etc/ssl/ \
    && openssl req -newkey rsa:4096 -nodes -sha256 -keyout server.key -subj "/O=$CERT_ORG_NAME/CN=$CERT_COMMON_NAME" -x509 -days 365 -out server.crt

COPY ./nginx.conf /etc/nginx/
COPY ./proxy.conf /etc/nginx/
