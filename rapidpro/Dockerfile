FROM python:3.9-slim AS base-py3.9
ARG RAPIDPRO_VERSION
RUN set -ex \
      && apt-get update \
      && apt-get install -y --no-install-recommends \
                gdal-bin \
                wget \
                postgresql-client \
                nodejs \
                npm \
                libxml2 \
                libpcre3 \
                openssl libgeos-dev \
      && npm install -g coffeescript less \
      && addgroup --system rapidpro \
      && adduser --system --ingroup rapidpro rapidpro \
      && pip install --no-cache-dir poetry \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*
USER rapidpro
WORKDIR /home/rapidpro
ENV HOME=/home/rapidpro
ENV POETRY_VIRTUALENVS_PATH=/home/rapidpro

FROM base-py3.9 AS build-py3.9
USER root
RUN set -ex \
        && apt-get update \
        && apt-get install -y \
                build-essential \
                libpq-dev \
                libjpeg-dev \
                libpng-dev \
                libfreetype-dev \
                libxslt-dev \
                libxml2-dev \
                zlib1g-dev \
                libffi-dev \
                libpcre2-dev \
                libreadline-dev \
                libncurses-dev \
                libgdal-dev \
               libzmq3-dev
USER rapidpro
RUN set -ex \
      && mkdir app \
      && wget -q -O rapidpro.tar.gz "https://github.com/rapidpro/rapidpro/archive/v${RAPIDPRO_VERSION}.tar.gz" \
      && tar -C app -xf rapidpro.tar.gz --strip-components=1 \
      && rm rapidpro.tar.gz \
      && export CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
      && cd app \
      && mkdir .npm \
      && npm install \
      && poetry remove codecov --lock --dev && poetry add "setuptools<81" --lock \
      && poetry install --sync --without dev

FROM base-py3.9
COPY --from=build-py3.9 /home/rapidpro/ .
WORKDIR app
COPY stack/settings.py ./temba
COPY server.sh celery.sh ./
EXPOSE 8000 8080
ENTRYPOINT ["/bin/sh"]
CMD ["-c", "./server.sh"]
