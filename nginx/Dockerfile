FROM nginx:alpine

RUN apk add --no-cache --virtual .deps openssl pwgen

ARG CERT_ORG_NAME
ARG CERT_ORG_UNIT
ARG CERT_COMMON_NAME
ARG CERT_COUNTRY
ARG CERT_LOCALITY

RUN set -ex \
    && mkdir -p /etc/ssl \
    && cd /etc/ssl/ \
    && pwgen -sy 12 1 > pass.txt \
    && openssl genpkey -aes-256-cbc -pass file:pass.txt -algorithm RSA -out server.pass.key -pkeyopt rsa_keygen_bits:4096 \
    && openssl rsa -passin file:pass.txt -in server.pass.key -out server.key \
    && rm pass.txt server.pass.key \
    && openssl req -new -key server.key -out server.csr -subj "/C=$CERT_COUNTRY/ST=$CERT_LOCALITY/L=$CERT_LOCATLITY/O=$CERT_ORG/OU=$CERT_ORG_UNIT/CN=$CERT_COMMON_NAME" \
    && openssl x509 -req -sha256 -days 360 -in server.csr -signkey server.key -out server.crt

COPY ./nginx.conf /etc/nginx/

