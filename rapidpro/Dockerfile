FROM rapidpro/rapidpro-base:v4

ARG TZ
ARG RAPIDPRO_VERSION
ARG RAPIDPRO_REPO

RUN set -ex \
  && apk add --no-cache \
    nodejs nodejs-npm libxml2 pcre openssl tar postgresql-client libmagic supervisor tzdata
RUN set -ex \
        && apk add --no-cache --virtual .build-deps \
                bash \
                patch \
                git \
                gcc \
                g++ \
                make \
                libc-dev \
                musl-dev \
                linux-headers \
                postgresql-dev \
                libjpeg-turbo-dev \
                libpng-dev \
                freetype-dev \
                libxslt-dev \
                libxml2-dev \
                zlib-dev \
                libffi-dev \
                pcre-dev \
                readline \
                readline-dev \
                ncurses \
                ncurses-dev \
                libzmq

ENV TZ=${TZ:-Africa/Nairobi}
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /root

ENV RAPIDPRO_VERSION="v$RAPIDPRO_VERSION"
ENV RAPIDPRO_REPO=${RAPIDPRO_REPO:-rapidpro/rapidpro}
ENV RAPIDPRO_REPO_URL="https://github.com/$RAPIDPRO_REPO/archive/$RAPIDPRO_VERSION.tar.gz"

RUN echo "Downloading RapidPro $RAPIDPRO_VERSION from $RAPIDPRO_REPO_URL" \
    && wget -q -O rapidpro.tar.gz $RAPIDPRO_REPO_URL \
    && mkdir rapidpro \
    && tar -C rapidpro -xf rapidpro.tar.gz --strip-components=1 \
    && rm rapidpro.tar.gz

WORKDIR rapidpro/

RUN set -ex \
    && npm config set unsafe-perm true \
    && npm install -g coffeescript less\
    && npm install \
    && pip install -r "pip-freeze.txt" \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

COPY stack/settings.py temba/
COPY startup.sh supervisor.conf  ./

EXPOSE 8000
ENTRYPOINT ["sh", "-c", "./startup.sh"]
