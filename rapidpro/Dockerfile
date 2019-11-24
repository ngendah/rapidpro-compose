FROM rapidpro/rapidpro-base:v4
ARG RAPIDPRO_VERSION
ENV PIP_RETRIES=120 \
    PIP_TIMEOUT=400 \
    PIP_DEFAULT_TIMEOUT=400 \
    C_FORCE_ROOT=1 \
    PIP_EXTRA_INDEX_URL="https://alpine-3.wheelhouse.praekelt.org/simple"

RUN set -ex \
  && apk add --no-cache \
    nodejs nodejs-npm libxml2 pcre openssl tar postgresql-client libmagic

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

WORKDIR /root

ARG RAPIDPRO_VERSION
ARG RAPIDPRO_REPO
ENV RAPIDPRO_VERSION=${RAPIDPRO_VERSION:-master}
ENV RAPIDPRO_REPO=${RAPIDPRO_REPO:-rapidpro/rapidpro}
RUN echo "Downloading RapidPro ${RAPIDPRO_VERSION} from https://github.com/$RAPIDPRO_REPO/archive/${RAPIDPRO_VERSION}.tar.gz" \
    && wget -q -O rapidpro.tar.gz "https://github.com/$RAPIDPRO_REPO/archive/${RAPIDPRO_VERSION}.tar.gz" \
    && mkdir rapidpro \
    && tar -C rapidpro -xf rapidpro.tar.gz --strip-components=1 \
    && rm rapidpro.tar.gz

WORKDIR rapidpro/
COPY stack/requirements.txt ./
RUN set -ex \
    && npm install -g coffee-script less bower \
    && npm install \
    && bower install --allow-root \
    && pip install "setuptools==33.1.1" \
    && pip install -r "requirements.txt" \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

COPY stack/settings.py temba/
COPY stack/500.html templates/
COPY stack/init_db.sql ./
COPY stack/clear-compressor-cache.py ./
COPY startup.sh ./

EXPOSE 8000
ENTRYPOINT ["sh", "-c", "./startup.sh"]
