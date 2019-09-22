FROM rapidpro/rapidpro-base:v4
ARG RAPIDPRO_VERSION
ENV PIP_RETRIES=120 \
    PIP_TIMEOUT=400 \
    PIP_DEFAULT_TIMEOUT=400 \
    C_FORCE_ROOT=1 \
    PIP_EXTRA_INDEX_URL="https://alpine-3.wheelhouse.praekelt.org/simple"

# Install `psql` command (needed for `manage.py dbshell` in stack/init_db.sql)
# Install `libmagic` (needed since rapidpro v3.0.64)
RUN set -ex \
  && apk add --no-cache libxml2 pcre nodejs-lts nodejs-npm openssl tar postgresql-client libmagic \
  && npm install -g coffee-script less bower

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
    && pip install "setuptools==33.1.1" \
    && pip install -r "requirements.txt" \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

RUN set -ex \
    && npm install npm@latest -g \
    && npm install \
    && bower install --allow-root

COPY stack/settings.py temba/
COPY stack/500.html templates/
COPY stack/init_db.sql ./
COPY stack/clear-compressor-cache.py ./
COPY startup.sh ./

EXPOSE 8000
ENTRYPOINT ["sh", "-c", "./startup.sh"]

